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

def color_test(camera):
    print("***/colorCorrection/lift***")
    print(camera.color_correction.get_lift())
    print(camera.color_correction.set_lift(luma=.5))
    time.sleep(.1)
    print(camera.color_correction.get_lift())
    print(camera.color_correction.set_lift(luma=0.0))
    print(camera.color_correction.get_gamma())
    print(camera.color_correction.get_gain())
    print(camera.color_correction.get_offset())
    print(camera.color_correction.get_contrast())
    print(camera.color_correction.get_color())
    print(camera.color_correction.get_luma_contribution())

    print(camera.video.get_iso())
    print(camera.video.get_gain())
    print(camera.video.get_white_balance())
    print(camera.video.get_white_balance_tint())
    print(camera.video.get_nd_filter())
    print(camera.video.get_nd_filter_display_mode())
    print(camera.get_shutter())
    print(camera.set_shutter(shutter_speed=1000))
    time.sleep(.1)
    print(camera.get_shutter())
    print(camera.set_shutter(shutter_speed=60))
    print(camera.video.get_auto_exposure())
    print(camera.video.do_auto_white_balance())

def main():
    if len(sys.argv) < 2:
        print("USAGE: ColorCorrectionTest.py CAMERA_IP_OR_HOSTNAME")
        return
    camera = BMCCCamera(sys.argv[1])
    color_test(camera)

if __name__ == '__main__':
    main()
