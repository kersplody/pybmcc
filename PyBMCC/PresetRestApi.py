#!/usr/bin/env python3
# coding: utf-8

import PresetControl.api.default_api as default_api
from PresetControl.rest import ApiException
import PyBMCC.Enums as Enums
import logging
from typing import Union
import time

class BMCCPreset:

    bmcc_camera = None
    preset_api_client = None

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.preset_api_client = default_api.DefaultApi()
        self.preset_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_presets(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.preset_api_client.presets_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def upload_preset(self,presetBinary=None):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.preset_api_client.presets_post(body=presetBinary)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_active_preset(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.preset_api_client.presets_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_active_preset(self,preset=None):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from PresetControl.models.active_preset import ActivePreset
            body = ActivePreset(preset=preset)
            result = self.preset_api_client.presets_active_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def download_preset(self,preset_name:str):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.preset_api_client.presets_preset_name_get(preset_name=preset_name)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def overwrite_preset(self,preset_name:str,preset=None):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from PresetControl.models.active_preset import ActivePreset
            body = ActivePreset(preset=preset)
            result = self.preset_api_client.presets_preset_name_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def delete_preset(self,preset_name:str=None):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.preset_api_client.presets_preset_name_delete(preset_name=preset_name)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0
