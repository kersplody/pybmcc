#!/usr/bin/env python3
# coding: utf-8

import ColorCorrectionControl.api.default_api as default_api
import PyBMCC.Enums as Enums
from ColorCorrectionControl.rest import ApiException
import logging
from typing import Union
import time


class BMCCColorCorrection:

    bmcc_camera = None
    color_correction_api_client = None

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.color_correction_api_client = default_api.DefaultApi()
        self.color_correction_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_lift(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.color_correction_api_client.color_correction_lift_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_lift(self,red=0.0, green=0.0, blue=0.0, luma=0.0):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from ColorCorrectionControl.models.lift import Lift
            body = Lift(red=red, green=green, blue=blue, luma=luma)
            result = self.color_correction_api_client.color_correction_lift_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_gamma(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.color_correction_api_client.color_correction_gamma_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_gamma(self,red=0.0, green=0.0, blue=0.0, luma=0.0):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from ColorCorrectionControl.models.gamma import Gamma
            body = Gamma(red=red, green=green, blue=blue, luma=luma)
            result = self.color_correction_api_client.color_correction_gamma_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_gain(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.color_correction_api_client.color_correction_gain_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_gain(self,red=0.0, green=0.0, blue=0.0, luma=0.0):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from ColorCorrectionControl.models.gain import Gain
            body = Gain(red=red, green=green, blue=blue, luma=luma)
            result = self.color_correction_api_client.color_correction_gain_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_offset(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.color_correction_api_client.color_correction_offset_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result


    def set_offset(self,red=0.0, green=0.0, blue=0.0, luma=0.0):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from ColorCorrectionControl.models.offset import Offset
            body = Offset(red=red, green=green, blue=blue, luma=luma)
            result = self.color_correction_api_client.color_correction_offset_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_contrast(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.color_correction_api_client.color_correction_contrast_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_contrast(self,pivot=0.5, adjust=1.0):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from ColorCorrectionControl.models.contrast import Contrast
            body = Contrast(pivot=pivot, adjust=adjust)
            result = self.color_correction_api_client.color_correction_contrast_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_color(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.color_correction_api_client.color_correction_color_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_color(self,hue=0.0, saturation=1.0):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from ColorCorrectionControl.models.color import Color
            body = Color(hue=hue, saturation=saturation)
            result = self.color_correction_api_client.color_correction_color_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_luma_contribution(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.color_correction_api_client.color_correction_luma_contribution_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_luma_contribution(self,luma_contribution=1.0):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from ColorCorrectionControl.models.luma_contribution import LumaContribution
            body = LumaContribution(luma_contribution=luma_contribution)
            result = self.color_correction_api_client.color_correction_luma_contribution_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0
