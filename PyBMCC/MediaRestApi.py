#!/usr/bin/env python3
# coding: utf-8

import MediaControl.api.default_api as default_api
import PyBMCC.Enums as Enums
from MediaControl.rest import ApiException
import logging
from typing import Union
import time


class BMCCMedia:

    bmcc_camera = None
    media_api_client = None
    primary_disk_id = None
    record_minutes = 0
    total_space = 0
    remaining_space = 0
    clip_count = 0
    disk_update_timestamp = 0
    device_format_key = None

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.media_api_client = default_api.DefaultApi()
        self.media_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_workingset(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.media_api_client.media_workingset_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        record_minutes = result.workingset[0].remaining_record_time
        total_space = result.workingset[0].total_space
        remaining_space = result.workingset[0].remaining_space
        clip_count = result.workingset[0].clip_count
        disk_update_timestamp = time.time()

        return result

    def get_active(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.media_api_client.media_active_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        self.primary_disk_id = result.device_name
        return result

    def set_active(self,workingset_index=0):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from MediaControl.models.media_active_body import MediaActiveBody
            body = MediaActiveBody(workingset_index=workingset_index)
            result = self.media_api_client.media_active_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_supported_filesystems(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.media_api_client.media_devices_doformat_supported_filesystems_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def get_device_info(self,device_name=None):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.media_api_client.media_devices_device_name_get(device_name=device_name)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def get_device_format_key(self,device_name=None):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.media_api_client.media_devices_device_name_doformat_get(device_name=device_name)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        self.device_format_key=result.key
        return result.key

    def do_device_format(self,key=None, filesystem=None, device_name=None, volume=None):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from MediaControl.models.device_name_doformat_body import DeviceNameDoformatBody
            body = DeviceNameDoformatBody(key=key, filesystem=filesystem, volume=volume)
            result = self.media_api_client.media_devices_device_name_doformat_put(device_name=device_name,body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0
