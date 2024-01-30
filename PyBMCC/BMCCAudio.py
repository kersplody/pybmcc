#!/usr/bin/env python3
# coding: utf-8

import AudioControl.api.default_api as default_api
from decimal import Decimal, ROUND_HALF_UP
import PyBMCC.Enums as Enums
from AudioControl.rest import ApiException
import logging
import json
from typing import Union
import time

from AudioControl import Description


class BMCCAudio:

    bmcc_camera = None
    audio_api_client = None

    channel_configuration = []
    channel_capabilities = []
    channel_supported_inputs = []
    channel_available = []

    def __init__(self, bmcc_camera):
        self.bmcc_camera = bmcc_camera
        self.audio_api_client = default_api.DefaultApi()
        self.audio_api_client.api_client.configuration.host=f"http://{bmcc_camera.host_or_ipaddr}/control/api/v1"

    def discover_channels(self):
        """Discover all audio channels, their configuration, and their features and updates the audio object state"""
        self.channel_configuration = []
        self.channel_capabilities = []
        self.channel_supported_inputs = []

        for channel in range(0,100):
            result=self.get_channel_input(channel)
            if result==-4: #done with camera channels
                return
            self.channel_configuration.append(result)
            self.channel_capabilities.append(self.get_channel_input_description(channel))
            self.channel_supported_inputs.append(self.get_channel_input_supported_inputs(channel))
            self.channel_available.append(self.get_channel_available(channel))

    def get_channel_input(self,channel:int=0) -> Union[int,str]:
        """Get the audio input (source and type) for the selected channel

        :param int channel: The index of the channel that its input is being controlled. (Channels index from 0) (required)
        :return: str the name of the input_channel or int error code. Possible values
              - None
              - Camera - Left
              - Camera - Right
              - Camera - Mono
              - XLR1 - Mic
              - XLR1 - Line
              - XLR2 - Mic
              - XLR2 - Line
              - 3.5mm Left - Line
              - 3.5mm Left - Mic
              - 3.5mm Right - Line
              - 3.5mm Right - Mic
              - 3.5mm Mono - Line
              - 3.5mm Mono - Mic
        """
        if self.bmcc_camera.state!=Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result=self.audio_api_client.audio_channel_channel_index_input_get(channel_index=channel)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result.input

    def set_channel_input(self,channel:int=0,input:str=None) -> int:
        """Set the audio input for the selected channel

         :param int channel: The index of the channel that its input is being controlled. (Channels index from 0) (required)
         :param str input: see get_channel_input for legal values

         :return: int status code
         """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from AudioControl.models.input import Input
            body=Input(input=input)
            result = self.audio_api_client.audio_channel_channel_index_input_put(channel_index=channel,body=body)
        except ValueError as ex:
            return -5 #bad input requested
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_channel_input_description(self,channel:int=0) -> Union[int,dict]:
        """Get the description of the current input of the selected channel
        :param int channel: The index of the channel that its input is being controlled. (Channels index from 0) (required)

        :return: dict description object or int error code
        """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.audio_api_client.audio_channel_channel_index_input_description_get(channel_index=channel)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return json.loads(self.audio_api_client.api_client.last_response.data)

    def get_channel_input_supported_inputs(self,channel:int=0) -> Union[int,str]:
        """Get the description of the current input of the selected channel
        :param int channel: The index of the channel that its input is being controlled. (Channels index from 0) (required)

        :return: dict description object or int error code
        """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.audio_api_client.audio_channel_channel_index_supported_inputs_get(channel_index=channel)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return json.loads(self.audio_api_client.api_client.last_response.data)

    def get_channel_input_level(self,channel:int=0) -> Union[int,float]:
        """Get the audio input level for the selected channel
        :param int channel: The index of the channel that its input is being controlled. (Channels index from 0) (required)

        :return: float normalised level or int error code
        """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.audio_api_client.audio_channel_channel_index_level_get(channel_index=channel)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result.normalised

    def set_channel_input_level(self,channel:int=0,gain:float=None,normalised:float=None) -> Union[int,str]:
        """Set the audio input level for the selected channel
         :param int channel: The index of the channel that its input is being controlled. (Channels index from 0) (required)
         :param float normalised: The normalised of this Level.
         :param float gain: The gain of this Level in db. Query audio channel capabilities for the valid range
         :return: float normalised level or int error code
         """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from AudioControl.models.level import Level
            body = Level(normalised=normalised,gain=gain)
            result = self.audio_api_client.audio_channel_channel_index_level_put(channel_index=channel,body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_channel_phantom_power(self,channel:int=0) -> Union[int,bool]:
        """Get the audio input phantom power for the selected channel if possible
        :param int channel_index: The index of the channel that its input is being controlled. (Channels index from 0) (required)

        :return: bool feature enabled or int error code
        """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.audio_api_client.audio_channel_channel_index_phantom_power_get(channel_index=channel)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_channel_phantom_power(self,channel:int=0,phantom_power=None) -> Union[int,bool]:
        """Set the audio input phantom power for the selected channel if possible
          :param int channel_index: The index of the channel that its input is being controlled. (Channels index from 0) (required)
          :param bool phantom_power: enable/disable phantom power feature
          :return: float normalised level or int error code
          """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from AudioControl.models.phantom_power import PhantomPower
            body = PhantomPower(phantom_power=phantom_power)
            result = self.audio_api_client.audio_channel_channel_index_level_put(channel_index=channel, body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        if self.audio_api_client.api_client.last_response.status==204:
            return -4
        return 0

    def get_channel_padding(self,channel:int=0) -> Union[int,bool]:
        """Get the audio input padding for the selected channel
        :param int channel_index: The index of the channel that its input is being controlled. (Channels index from 0) (required)

        :return: bool feature enabled or int error code
        """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.audio_api_client.audio_channel_channel_index_padding_get(channel_index=channel)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_channel_padding(self,channel:int=0,padding:bool=None) -> Union[int,bool]:
        """Set the audio input padding for the selected channel
          :param int channel_index: The index of the channel that its input is being controlled. (Channels index from 0) (required)
          :param bool padding: enable/disable padding
          :return: float normalised level or int error code
          """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from AudioControl.models.padding import Padding
            body = Padding(padding=padding)
            result = self.audio_api_client.audio_channel_channel_index_padding_put(channel_index=channel, body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_channel_low_cut_filter(self,channel:int=0) -> Union[int,bool]:
        """Get the audio input low cut filter for the selected channel
        :param int channel_index: The index of the channel that its input is being controlled. (Channels index from 0) (required)

        :return: bool feature enabled or int error code
        """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.audio_api_client.audio_channel_channel_index_low_cut_filter_get(channel_index=channel)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result

    def set_channel_low_cut_filter(self,channel:int=0,low_cut_filter:bool=None) -> Union[int,bool]:
        """Set the audio input low cut filter for the selected channel
          :param int channel_index: The index of the channel that its input is being controlled. (Channels index from 0) (required)
          :param bool low_cut_filter: enable/disable low_cut_filter
          :return: float normalised level or int error code
          """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            from AudioControl.models.low_cut_filter import LowCutFilter
            body = LowCutFilter(low_cut_filter=low_cut_filter)
            result = self.audio_api_client.audio_channel_channel_index_low_cut_filter_put(channel_index=channel, body=body)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return 0

    def get_channel_available(self,channel:int=0) -> Union[int,bool]:
        """Get the audio input's current availability for the selected channel. If unavailable, the source will be muted
        :param int channel_index: The index of the channel that its input is being controlled. (Channels index from 0) (required)

        :return: dict description object or int error code

        """
        if self.bmcc_camera.state != Enums.CameraState.CONNECTED and not self.bmcc_camera.try_when_disconnected:
            return -2
        try:
            result = self.audio_api_client.audio_channel_channel_index_available_get(channel_index=channel)
        except ApiException as ex:
            return -4
        except Exception as ex:
            self.bmcc_camera.handle_exception(ex)
            return -1
        return result
