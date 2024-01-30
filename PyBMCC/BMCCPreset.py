#!/usr/bin/env python3
# coding: utf-8

import PresetControl.api.default_api as default_api
from decimal import Decimal, ROUND_HALF_UP
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
        return

    def upload_preset(self):
        return

    def get_active_preset(self):
        return

    def set_active_preset(self):
        return

    def overwrite_preset(self):
        return

    def delete_preset(self):
        return
