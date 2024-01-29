#!/usr/bin/env python3
# coding: utf-8

from PyBMCC import BMCCCamera
import logging
import time
import sys
from PyBMCC.Enums import CommandStauts,TransportResponse

logging.basicConfig(level=logging.DEBUG)

MSG1="Current transport {0}: {1}"
MSG2="Commanding transport {0} to {1}.... RESULT: {2}"
MSG3="Commanding transport {0}... RESULT: {1}"

def transport_test(camera):

    #STATUS
    logging.info(MSG1.format("status",camera.transport.get_status()))
    camera.transport.set_status(TransportResponse.Output)
    logging.info(MSG1.format("is stopped",camera.transport.get_stop()))
    camera.transport.set_stop()
    logging.info(MSG1.format("is playing",camera.transport.get_play()))
    camera.transport.set_play()
    logging.info(MSG1.format("playback state",camera.transport.get_playback()))
    logging.info(MSG1.format("record state", camera.is_recording()))

    logging.info(MSG1.format("timecode", camera.get_timecode()))
    time.sleep(1)
    logging.info(MSG1.format("timecode", camera.get_timecode()))
    logging.info(MSG1.format("timecode source", camera.transport.get_timecode_source()))
    logging.info(MSG2.format("recording with no clip name", "on", camera.record_start()))
    time.sleep(0.5)
    logging.info(MSG1.format("record state", camera.is_recording()))
    time.sleep(3.0)
    logging.info(MSG2.format("recording with no clip name", "off", camera.record_stop()))
    time.sleep(0.5)
    logging.info(MSG1.format("record state", camera.is_recording()))
    logging.info(MSG2.format("recording with clip name", "on", camera.record_start(str(time.time()))))
    time.sleep(3.0)
    logging.info(MSG2.format("recording with no clip name", "off", camera.record_stop()))



def main():
    if len(sys.argv) < 2:
        print("USAGE: TransportTest.py CAMERA_IP_OR_HOSTNAME")
        return
    camera = BMCCCamera(sys.argv[1])
    transport_test(camera)

if __name__ == '__main__':
    main()
