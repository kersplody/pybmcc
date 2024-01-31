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

def media_test(camera):
    print(camera.media.get_workingset())
    print(camera.media.get_active())
    print(camera.media.get_supported_filesystems())
    print(camera.media.get_device_info(camera.media.primary_disk_id))
    print(camera.media.get_device_format_key(camera.media.primary_disk_id))

def main():
    if len(sys.argv) < 2:
        print("USAGE: ColorCorrectionTest.py CAMERA_IP_OR_HOSTNAME")
        return
    camera = BMCCCamera(sys.argv[1])
    media_test(camera)

if __name__ == '__main__':
    main()
