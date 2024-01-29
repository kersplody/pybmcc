#!/usr/bin/env python3
# coding: utf-8

import TransportControl.api.default_api as default_api
from typing import Union
import PyBMCC.Enums as Enums
import logging
import time

class BMCCTransport:

    bmcc_camera = None
    transport_api_client = None
    try_when_disconnected = False

    mode_update_timestamp = 0
    mode = Enums.TransportResponse.UNKNOWN
    status_update_timestamp = 0
    status = Enums.TransportStatus.UNKNOWN
    timecode_update_timestamp = 0
    raw_timecode = 0
    raw_clip_timecode = 0
    timecode = "00:00:00:00"
    clip_timecode = "00:00:00:00"

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.transport_api_client = default_api.DefaultApi()
        self.transport_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def get_status(self) -> Union[int,str]:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            result=self.transport_api_client.transports0_get()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        self.mode_update_timestamp=time.time()
        self.mode=Enums.TransportResponse[result.mode]
        return self.mode.name

    def set_status(self, transport_status:Enums.TransportResponse) -> int:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        if transport_status is Enums.TransportResponse.UNKNOWN:
            logging.warning("UNKNOWN cannot be used to set the TransportResponse")
            return -3

        try:
            from TransportControl.models.transports0_body import Transports0Body
            body = Transports0Body(transport_status.name)
            result = self.transport_api_client.transports0_put(body=body)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        return 0

    def get_stop(self) -> Union[int,bool]:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            result=self.transport_api_client.transports0_stop_get()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        if result:
            self.status=Enums.TransportStatus.STOP
        return result

    def set_stop(self) -> int:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2

        try:
            result = self.transport_api_client.transports0_stop_put()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        return 0

    def get_play(self) -> Union[int,bool]:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            result=self.transport_api_client.transports0_play_get()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        if result:
            self.status=Enums.TransportStatus.PLAY
        return result

    def set_play(self) -> int:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            result = self.transport_api_client.transports0_play_put()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        return 0

    def get_playback(self) -> Union[int,dict]:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            result=self.transport_api_client.transports0_playback_get()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        return result

    def set_playback(self,type:Enums.TransportPlayback=None,loop:bool=None,singleClip:bool=None,speed:float=None,position:int=None) -> int:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            from TransportControl.models.playback import Playback
            body = Playback(type=type,loop=loop,singleClip=singleClip,speed=speed,position=position)
            result = self.transport_api_client.transports0_playback_put()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        return 0

    def get_record(self) -> Union[int,bool]:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            result=self.transport_api_client.transports0_record_get()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        if result:
            self.status=Enums.TransportStatus.RECORD
        else:
            self.status = Enums.TransportStatus.PASSTHROUGH
        return result.recording

    def set_record(self,record:bool=False,clip_name:str=None) -> int:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            from TransportControl.models.record import Record
            body = Record(recording=record,clip_name=clip_name)
            result = self.transport_api_client.transports0_record_put(body=body)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        return 0

    def get_timecode(self) -> Union[int,str]:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            result=self.transport_api_client.transports0_timecode_get()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1

        self.timecode_update_timestamp = 0
        self.raw_timecode = result.timecode
        self.raw_clip_timecode = result.clip
        self.timecode = dec_to_timecode(result.timecode)
        self.clip_timecode = dec_to_timecode(result.clip)

        return self.timecode

    def get_timecode_source(self) -> Union[int,str]:
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.try_when_disconnected:
            return -2
        try:
            result=self.transport_api_client.transports0_timecode_source_get()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
            self.bmcc_camera.mark_disconnected()
            return -1
        return Enums.TimecodeSource[result.timecode].name

def dec_to_timecode(decimal_encoded_timecode):
    n=int(decimal_encoded_timecode)&2147483647 #mask highest bit
    timecode=""
    even=False
    for x in range(0,8):
        digit=n&0b1111
        n=n>>4
        timecode+=str(digit)
        if even and not x==7:
            timecode+=":"
        even=~even
    timecode=timecode[::-1]
    return timecode
