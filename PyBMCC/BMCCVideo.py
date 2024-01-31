#!/usr/bin/env python3
# coding: utf-8

import VideoControl.api.default_api as default_api
from VideoControl.rest import ApiException
import PyBMCC.Enums as Enums
import logging
from typing import Union
import time


class BMCCVideo:

    bmcc_camera = None
    video_api_client = None

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.video_api_client = default_api.DefaultApi()
        self.video_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_iso(self) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.video_api_client.video_iso_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_iso(self,iso:int=None) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from VideoControl.models.video_iso_body import VideoIsoBody
            body = VideoIsoBody(iso=iso)
            result = self.video_api_client.video_iso_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_gain(self) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.video_api_client.video_gain_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_gain(self,gain=None) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from VideoControl.models.video_gain_body import VideoGainBody
            body = VideoGainBody(gain=gain)
            result = self.video_api_client.video_gain_set(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_white_balance(self) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.video_api_client.video_white_balance_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_white_balance(self,white_balance=None) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from VideoControl.models.video_white_balance_body import VideoWhiteBalanceBody
            body = VideoWhiteBalanceBody(white_balance=white_balance)
            result = self.video_api_client.video_iso_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def do_auto_white_balance(self) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.video_api_client.video_white_balance_do_auto_put()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_white_balance_tint(self) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.video_api_client.video_white_balance_tint_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_white_balance_tint(self,white_balance_tint=None) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from VideoControl.models.video_white_balance_tint_body import VideoWhiteBalanceTintBody
            body = VideoWhiteBalanceTintBody(white_balance_tint=white_balance_tint)
            result = self.video_api_client.video_iso_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_nd_filter(self) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.video_api_client.video_nd_filter_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_nd_filter(self,stop:int=None) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from VideoControl.models.video_nd_filter_body import VideoNdFilterBody
            body = VideoNdFilterBody(stop=None)
            result = self.video_api_client.video_iso_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_nd_filter_display_mode(self) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.video_api_client.video_nd_filter_display_mode_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result
    def get_nd_filter_display_mode(self,stop:int=None) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from VideoControl.models.video_nd_filter_body import VideoNdFilterBody
            body = VideoNdFilterBody(stop=stop)
            result = self.video_api_client.video_iso_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_shutter(self) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.video_api_client.video_shutter_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result
    def set_shutter(self,shutter_speed=None, shutter_angle=None) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from VideoControl.models.video_shutter_body import VideoShutterBody
            body = VideoShutterBody(shutter_speed=shutter_speed, shutter_angle=shutter_angle)
            result = self.video_api_client.video_iso_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_auto_exposure(self) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.video_api_client.video_auto_exposure_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def put_auto_exposure(self,mode) -> int:
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from VideoControl.models.video_auto_exposure_body import VideoAutoExposureBody
            body = VideoAutoExposureBody(mode=None)
            result = self.video_api_client.video_iso_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0