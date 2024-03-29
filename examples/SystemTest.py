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

def system_test(camera):

    #STATUS
    logging.info(MSG2.format("video format", "29.97",camera.system.set_video_format(frame_rate=29.97))) #not implemented
    logging.info(MSG2.format("format codec", "BRaw:Q3",camera.system.set_format(codec="BRaw:Q3",frame_rate=29.97))) #not implemented

    logging.info(MSG1.format("system",camera.system.get_system()))
    logging.info(MSG1.format("supported codec formats",camera.system.get_supported_codec_formats()))
    logging.info(MSG1.format("supported video formats", camera.system.get_supported_video_formats()))
    logging.info(MSG1.format("codec formats", camera.system.get_codec_format()))
    logging.info(MSG1.format("video formats", camera.system.get_video_format()))
    logging.info(MSG1.format("format", camera.system.get_format()))
    logging.info(MSG1.format("events", camera.event.get_events()))
    logging.info(MSG1.format("timeline get", camera.timeline.get_timeline()))
    logging.info(MSG1.format("timeline get", camera.timeline.append_timeline(15)))
    logging.info(MSG1.format("timeline delete", camera.timeline.delete_timeline()))

    #ATEM ID
    id=camera.system.get_atem_id()
    logging.info(MSG1.format("ATEM ID", id))
    logging.info(MSG2.format("ATEM ID", 5, camera.system.set_atem_id(5)))
    time.sleep(1)
    logging.info(MSG1.format("ATEM ID", camera.system.get_atem_id()))
    logging.info(MSG2.format("ATEM ID", id, camera.system.set_atem_id(id)))
    time.sleep(1)
    logging.info(MSG1.format("ATEM ID", camera.system.get_atem_id()))

    #CLIPS
    logging.info(MSG1.format("clips", camera.system.get_clips()))
def main():
    if len(sys.argv) < 2:
        print("USAGE: TransportTest.py CAMERA_IP_OR_HOSTNAME")
        return
    camera = BMCCCamera(sys.argv[1])
    system_test(camera)

if __name__ == '__main__':
    main()
