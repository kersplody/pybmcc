#!/usr/bin/env python3
# coding: utf-8

from PyBMCC import BMCCCamera
import logging
import time
import sys
from PyBMCC.Enums import CommandStauts,TransportResponse

logging.basicConfig(level=logging.DEBUG)

MSG1="Current audio {0}: {1}"
MSG2="Commanding audio {0} to {1}.... RESULT: {2}"
MSG3="Commanding audio {0}... RESULT: {1}"

def audio_test(camera):
    print("***/audio/channel/{channelIndex}/input***")
    print(camera.audio.get_channel_input(2))
    print(camera.audio.set_channel_input(0,"None"))
    print(camera.audio.get_channel_input(0))
    time.sleep(.25)
    print(camera.audio.set_channel_input(0,"Camera - Left"))
    print(camera.audio.get_channel_input(0))
    print(camera.audio.set_channel_input(0,"asdasdasf"))
    print("***/audio/channel/{channelIndex}/input/description***")
    print(camera.audio.get_channel_input_description(0))
    print(camera.audio.get_channel_input_description(1))
    print(camera.audio.get_channel_input_description(2))
    print("***/audio/channel/{channelIndex}/input/supportedInputs***")
    print(camera.audio.get_channel_input_supported_inputs(0))
    print(camera.audio.get_channel_input_supported_inputs(1))
    print(camera.audio.get_channel_input_supported_inputs(2))
    print("***/audio/channel/{channelIndex}/input/available***")
    print(camera.audio.get_channel_available(0))
    print(camera.audio.get_channel_available(1))
    print(camera.audio.get_channel_available(2))
    print("***/audio/channel/{channelIndex}/input/level***")
    print(camera.audio.get_channel_input_level(0))
    print(camera.audio.set_channel_input_level(0,normalised=1.0))
    time.sleep(.1)
    print(camera.audio.get_channel_input_level(0))
    print(camera.audio.set_channel_input_level(0, normalised=0.5))
    print(camera.audio.get_channel_input_level(0))
    print("***/audio/channel/{channelIndex}/phantomPower***")
    print(camera.audio.get_channel_phantom_power(0))
    print(camera.audio.set_channel_phantom_power(0,"true"))
    print("***/audio/channel/{channelIndex}/padding***")
    print(camera.audio.get_channel_padding(0))
    print(camera.audio.set_channel_padding(0,"true"))
    print("***/audio/channel/{channelIndex}/lowCutFilter***")
    print(camera.audio.get_channel_low_cut_filter(0))
    print(camera.audio.set_channel_low_cut_filter(0,"true"))
def main():
    if len(sys.argv) < 2:
        print("USAGE: TransportTest.py CAMERA_IP_OR_HOSTNAME")
        return
    camera = BMCCCamera(sys.argv[1])
    audio_test(camera)

if __name__ == '__main__':
    main()
