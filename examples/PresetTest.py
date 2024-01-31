#!/usr/bin/env python3
# coding: utf-8

from PyBMCC import BMCCCamera
import logging
import time
import sys
from PyBMCC.Enums import CommandStauts,TransportResponse

logging.basicConfig(level=logging.DEBUG)

MSG1="Current system {0}: {1}"
MSG2="Commanding system {0} to {1}.... RESULT: {2}"
MSG3="Commanding system {0}... RESULT: {1}"

def preset_test(camera):
    print(camera.preset.get_presets())
    print(camera.preset.get_active_preset())
    print(camera.preset.set_active_preset(preset='Preset 2.cset'))


def main():
    if len(sys.argv) < 2:
        print("USAGE: PresetTest.py CAMERA_IP_OR_HOSTNAME")
        return
    camera = BMCCCamera(sys.argv[1])
    preset_test(camera)

if __name__ == '__main__':
    main()
