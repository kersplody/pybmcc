#!/usr/bin/env python3
# coding: utf-8

import VideoControl.api.default_api as default_api
from decimal import Decimal, ROUND_HALF_UP
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
        return

    def set_iso(self,iso:int=None) -> int:
        return

    def get_gain(self) -> int:
        return

    def set_gain(self,gain:int=None) -> int:
        return

    def get_white_balance(self) -> int:
        return

    def set_white_balance(self,white_balanc:int=None) -> int:
        return

    def do_auto_white_balance(self) -> int:
        return

    def get_white_balance_tint(self) -> int:
        return

    def set_white_balance_tint(self,tint:int=None) -> int:
        return

    def get_nd_filter(self) -> int:
        return

    def set_nd_filter(self,stop:int=None) -> int:
        return

    def get_nd_filter_display_mode(self) -> int:
        return

    def get_nd_filter_display_mode(self,display_mode:str=None) -> int:
        return

    def get_shutter(self) -> int:
        return

    def put_shutter(self) -> int:
        return

    def get_auto_exposure(self) -> int:
        return

    def put_auto_exposure(self,mode,type) -> int:
        return