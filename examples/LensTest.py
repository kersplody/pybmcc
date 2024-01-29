#!/usr/bin/env python3
# coding: utf-8

from PyBMCC import BMCCCamera
import logging
import time
import sys
from PyBMCC.Enums import CommandStauts
from pprint import pformat

logging.basicConfig(level=logging.DEBUG)

MSG1="Current lens {0}: {1:.1f}"
MSG2="Commanding lens {0} to {1}.... RESULT: {2}"
MSG3="Commanding lens {0}... RESULT: {1}"

def lens_test(camera):

    logging.info(f"Getting Lens F-Stops...")
    logging.info(pformat(camera.lens.get_iris_stops()))

    #FOCUS
    logging.info(MSG1.format("focus",camera.get_focus()))

    logging.info(MSG2.format("focus", 0.0,CommandStauts(camera.set_focus(0.0)).name))
    time.sleep(1) # Wait for lens movement
    logging.info(MSG1.format("focus",camera.get_focus()))

    logging.info(MSG2.format("focus", 1.0,CommandStauts(camera.set_focus(1.0)).name))
    time.sleep(1) # Wait for lens movement
    logging.info(MSG1.format("focus",camera.get_focus()))

    logging.info(MSG3.format("autofocus",CommandStauts(camera.do_auto_focus()).name))
    time.sleep(1.25) # Wait for lens movement
    logging.info(MSG1.format("focus",camera.get_focus()))

    #ZOOM
    logging.info(MSG1.format("zoom", camera.get_zoom()))

    logging.info(MSG2.format("zoom", 1.0, CommandStauts(camera.set_zoom(normalised=1.0)).name))
    time.sleep(1.0) # Wait for lens movement
    logging.info(MSG1.format("zoom",camera.get_zoom()))

    logging.info(MSG2.format("zoom", 0.0, CommandStauts(camera.set_zoom(normalised=0.0)).name))
    time.sleep(1.0) # Wait for lens movement
    logging.info(MSG1.format("zoom",camera.get_zoom()))

    logging.info(MSG2.format("zoom", 0.5, CommandStauts(camera.set_zoom(normalised=0.5)).name))
    time.sleep(0.5) # Wait for lens movement
    logging.info(MSG1.format("zoom",camera.get_zoom()))

    #IRIS

    logging.info(MSG1.format("iris", camera.get_iris()))

    logging.info(MSG2.format("iris", "f8.0" , CommandStauts(camera.set_iris(8.0)).name))
    time.sleep(1.5) # Wait for lens movement
    logging.info(MSG1.format("iris",camera.get_iris()))

    logging.info(MSG2.format("iris", 0.0, CommandStauts(camera.set_iris(normalised=0.0)).name))
    time.sleep(1.0) # Wait for lens movement
    logging.info(MSG1.format("iris",camera.get_iris()))

    logging.info(MSG2.format("iris", 1.0, CommandStauts(camera.set_iris(normalised=1.0)).name))
    time.sleep(0.5) # Wait for lens movement
    logging.info(MSG1.format("iris",camera.get_iris()))

def main():
    if len(sys.argv) < 2:
        print("USAGE: LensTest.py CAMERA_IP_OR_HOSTNAME")
        return
    camera = BMCCCamera(sys.argv[1])
    lens_test(camera)

if __name__ == '__main__':
    main()
