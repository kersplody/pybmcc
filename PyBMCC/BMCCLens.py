#!/usr/bin/env python3
# coding: utf-8

import LensControl.api.default_api as default_api
from decimal import Decimal, ROUND_HALF_UP
import PyBMCC.Enums as Enums
import logging
import time


class BMCCLens:

    bmcc_camera = None
    lens_api_client = None

    aperture_update_timestamp = 0
    continuous_aperture_auto_exposure = Enums.UNKNOWN
    aperture_stop = -1
    aperture_normalised = Enums.UNKNOWN
    aperture_number = -1
    focal_length_update_timestamp = -1
    focal_length = -1
    focal_length_normalised = -1
    focus_update_timestamp = -1
    focus = -1
    iris_stops = []

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.lens_api_client = default_api.DefaultApi()
        self.lens_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_iris_stops(self) -> list[float]:
        iris_stops=list()

        self.set_iris(normalised=0.0)
        time.sleep(.5)

        for iris in [x * .05 for x in range(21)]:
            self.set_iris(normalised=iris)
            time.sleep(.25)
            stop = float(Decimal(Decimal(self.get_iris()).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)))
            if stop not in iris_stops:
                iris_stops.append(stop)

        self.iris_stops=list(iris_stops)
        return self.iris_stops

    def get_iris(self) -> float:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result=self.lens_api_client.lens_iris_get()
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        self.aperture_update_timestamp=time.time()
        self.continuous_aperture_auto_exposure=result.continuous_aperture_auto_exposure
        self.aperture_stop=result.aperture_stop
        self.aperture_normalised=result.normalised
        self.aperture_number=result.aperture_number
        return result.aperture_stop

    def set_iris(self, aperture_stop:float=None, normalised:float=None, aperture_number:int=None) -> int:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        if aperture_stop is None and normalised is None and aperture_number is None:
            logging.warning("One of apertureStop, normalised, or apertureNumber must be set")
            return -3

        try:
            from LensControl.models.lens_iris_body import LensIrisBody
            body = LensIrisBody(aperture_stop, normalised, aperture_number)
            result = self.lens_api_client.lens_iris_put(body=body)
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_zoom(self) -> float:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.lens_api_client.lens_zoom_get()
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        self.focal_length_update_timestamp = time.time()
        self.focal_length = result.focal_length
        self.focal_length_normalised = result.normalised
        return result.focal_length

    def set_zoom(self,focal_length:float=None,normalised:float=None) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        if focal_length is None and normalised is None:
            logging.warning("One of focal_length or normalised must be set")
            return -3
        try:
            from LensControl.models.lens_zoom_body import LensZoomBody
            body = LensZoomBody(focal_length, normalised)
            result = self.lens_api_client.lens_iris_put(body=body)
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_focus(self) -> float:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.lens_api_client.lens_focus_get()
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        self.focus_update_timestamp = time.time()
        self.focus = result.focus
        return result.focus

    def set_focus(self, focus:float) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from LensControl.models.lens_focus_body import LensFocusBody
            body = LensFocusBody(focus)
            result = self.lens_api_client.lens_focus_put(body=body)
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def do_auto_focus(self) -> int:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2

        try:
            result = self.lens_api_client.lens_focus_do_auto_focus_put()
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0