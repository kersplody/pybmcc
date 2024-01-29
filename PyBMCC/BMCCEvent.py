#!/usr/bin/env python3
# coding: utf-8

import EventControl.api.default_api as default_api
import PyBMCC.Enums as Enums

class BMCCEvent:

    bmcc_camera = None
    event_api_client = None

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.event_api_client = default_api.DefaultApi()
        self.event_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_events(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.event_api_client.event_list_get()
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result
