#!/usr/bin/env python3
# coding: utf-8

import TimelineControl.api.default_api as default_api
import PyBMCC.Enums as Enums
from TimelineControl.rest import ApiException

class BMCCTimeline:

    bmcc_camera = None
    timeline_api_client = None

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.timeline_api_client = default_api.DefaultApi()
        self.timeline_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_timeline(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.timeline_api_client.timelines0_get()
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def append_timeline(self, clips):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            import json
            body={}
            body['clips']=clips
            result = self.timeline_api_client.timelines0_add_post(body=body)
        except ApiException as ex:
            if ex.status==501:
                return -4
            return -5
        except Exception as ex:
            import traceback
            print(traceback.format_exc())
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def delete_timeline(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.timeline_api_client.timelines0_delete()
        except ApiException as ex:
            if ex.status==501:
                return -4
            return -5
        except Exception as ex:
            import traceback
            print(traceback.format_exc())
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0