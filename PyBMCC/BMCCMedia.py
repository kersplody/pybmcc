#!/usr/bin/env python3
# coding: utf-8

import MediaControl.api.default_api as default_api
from decimal import Decimal, ROUND_HALF_UP
import PyBMCC.Enums as Enums
import logging
from typing import Union
import time


class BMCCMedia:

    bmcc_camera = None
    media_api_client = None

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.media_api_client = default_api.DefaultApi()
        self.media_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_workingset(self):
        return
    def get_active(self):
        return

    def put_active(self):
        return

    def get_active(self):
        return

    def get_supported_filesystems(self):
        return

    def get_device_info(self):
        return

    def get_device_format_key(self):
        return

    def get_do_device_format(self):
        return