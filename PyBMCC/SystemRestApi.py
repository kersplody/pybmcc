#!/usr/bin/env python3
# coding: utf-8

import SystemControl.api.default_api as default_api
from typing import Union
import json
import PyBMCC.Enums as Enums
from SystemControl.rest import ApiException
import time

class BMCCSystem:

    bmcc_camera = None
    system_api_client = None

    supported_formats=None
    supported_codecs=[]
    supported_frame_rates=[]
    codec = Enums.UNKNOWN
    frame_rate = 0.0
    record_resolution = [0,0]
    sensor_resolution = [0,0]
    off_speed_enabled = False
    off_speed_frame_rate = 0.0
    max_off_speed_frame_rate = 0.0
    min_off_speed_frame_rate = 0.0
    clip_list = None

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.system_api_client = default_api.DefaultApi()
        self.system_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_system(self) -> Union[int,dict]:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result=self.system_api_client.system_get()
        except TypeError as ex: #camera returns an undefined 204 response which is undefined and crashes swagger
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def get_supported_codec_formats(self):
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result=self.system_api_client.system_supported_formats_get()
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status==501:
            return -4
        try:
            self.supported_codecs=result.supported_formats[0].codecs
            self.supported_frame_rates=result.supported_formats[0].frame_rates
            self.supported_formats=result
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def get_codec_format(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.system_api_client.system_codec_format_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            import traceback
            print(traceback.format_exc())
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status == 501:
            return -4
        return result

    def set_codec_format(self,codec=None,container=None):
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from SystemControl.models.codec_format import CodecFormat
            body = CodecFormat(codec=codec,container=container)
            result=self.system_api_client.system_codec_format_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status==501:
            return -4
        return result

    def get_video_format(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.system_api_client.system_video_format_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            import traceback
            print(traceback.format_exc())
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status == 501:
            return -4
        return result

    def set_video_format(self,frame_rate=None, height=None, width=None, interlaced=None):
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from SystemControl.models.video_format import VideoFormat
            body = VideoFormat(frame_rate=frame_rate, height=height, width=width, interlaced=interlaced)
            result=self.system_api_client.system_video_format_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status==501:
            return -4
        return result

    def get_supported_video_formats(self):
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.system_api_client.system_supported_video_formats_get()
        except ApiException as ex:
            return -4
        except Exception as ex:
            import traceback
            print(traceback.format_exc())
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status == 501:
            return -4
        return result

    def get_format(self):
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result=self.system_api_client.system_format_get()
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status==501:
            return -4
        try:
            self.frame_rate=result.frame_rate
            self.codec=result.codec
            self.max_off_speed_frame_rate=result.max_off_speed_frame_rate
            self.min_off_speed_frame_rate=result.min_off_speed_frame_rate
            self.off_speed_enabled=result.off_speed_enabled
            self.record_resolution[0]=result.record_resolution.width
            self.record_resolution[1]=result.record_resolution.height
            self.sensor_resolution[0]=result.record_resolution.width
            self.sensor_resolution[1]=result.record_resolution.height
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result.codec+" "+str(result.frame_rate)+" "+str(self.record_resolution[0])+"x"+str(self.record_resolution[1])

    def set_format(self,codec=None, frame_rate=None, max_off_speed_frame_rate=None, min_off_speed_frame_rate=None, off_speed_enabled=None, off_speed_frame_rate=None, record_resolution=None, sensor_resolution=None):
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from SystemControl.models.format import Format
            body = Format(
                codec=codec,
                frame_rate=frame_rate,
                max_off_speed_frame_rate=max_off_speed_frame_rate,
                min_off_speed_frame_rate=min_off_speed_frame_rate,
                off_speed_enabled=off_speed_enabled,
                off_speed_frame_rate=off_speed_frame_rate,
                record_resolution=record_resolution,
                sensor_resolution=sensor_resolution)
            result=self.system_api_client.system_video_format_put(body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status==501:
            return -4
        return result

    ### Bonus undocumented API features
    def get_atem_id(self):
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            header_params = {}
            header_params['Content-Type'] = self.system_api_client.api_client.select_header_content_type(  # noqa: E501
                ['application/json'])

            result=self.system_api_client.api_client.call_api(
                '/camera/id', 'GET',
                {},
                [],
                {},
                body=None,
                post_params=[],
                files={},
                response_type=None,  # noqa: E501
                auth_settings=[],
                async_req=None,
                _return_http_data_only=True,
                _preload_content=True,
                _request_timeout=None,
                collection_formats={})
        except Exception as ex:
            import traceback
            print(traceback.format_exc())
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status==501:
            return -4

        try:
            result=self.system_api_client.api_client.last_response.data
            id=json.loads(result)['id']
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex,False)
            return -1
        self.bmcc_camera.atem_id=id
        return id

    def set_atem_id(self,atem_id:int=1):
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            body={}
            body['id']=atem_id

            header_params = {}
            header_params['Content-Type'] = 'application/json'

            result=self.system_api_client.api_client.call_api(
                '/camera/id', 'PUT',
                {},
                [],
                {},
                body=body,
                post_params=[],
                files={},
                response_type=None,  # noqa: E501
                auth_settings=[],
                async_req=None,
                _return_http_data_only=True,
                _preload_content=True,
                _request_timeout=None,
                collection_formats={})
        except Exception as ex:
            import traceback
            print(traceback.format_exc())
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status==501:
            return -4
        self.bmcc_camera.atem_id = atem_id
        return 0

    def get_clips(self,only_last=False):
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            header_params = {}
            header_params['Content-Type'] = self.system_api_client.api_client.select_header_content_type(  # noqa: E501
                ['application/json'])

            result=self.system_api_client.api_client.call_api(
                '/clips/list', 'GET',
                {},
                [],
                {},
                body=None,
                post_params=[],
                files={},
                response_type=None,  # noqa: E501
                auth_settings=[],
                async_req=None,
                _return_http_data_only=True,
                _preload_content=True,
                _request_timeout=None,
                collection_formats={})
        except ApiException as ex:
            # todo: handle more error states
            return -1
        except Exception as ex:
            import traceback
            print(traceback.format_exc())
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.system_api_client.api_client.last_response.status==501:
            return -4

        try:
            result=self.system_api_client.api_client.last_response.data
            result=json.loads(result)
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex,False)
            return -1
        self.clip_list=result['clipList']
        if only_last:
            if 'clipList' not in result:
                return -1
            if len(result['clipList']) ==0:
                return  -1
            latest_clip_idx=-1
            for clip in result['clipList']:
                if clip['clipUniqueId']-1 > latest_clip_idx:
                    latest_clip_idx=clip['clipUniqueId']-1
            return result['clipList'][latest_clip_idx]['filePath']
        return result
