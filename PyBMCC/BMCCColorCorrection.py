#!/usr/bin/env python3
# coding: utf-8

import ColorCorrectionControl.api.default_api as default_api
from decimal import Decimal, ROUND_HALF_UP
import PyBMCC.Enums as Enums
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
        return

    def put_lift(self):
        return

    def get_gamma(self):
        return

    def put_gamma(self):
        return

    def get_gain(self):
        return

    def put_gain(self):
        return

    def get_offset(self):
        return

    def put_offset(self):
        return

    def get_contrast(self):
        return

    def put_contrast(self):
        return

    def get_color(self):
        return

    def put_color(self):
        return

    def get_luma_contribution(self):
        return

    def set_luma_contribution(self):
        return
