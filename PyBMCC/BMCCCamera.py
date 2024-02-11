#!/usr/bin/env python3
# coding: utf-8

"""
BMCCCamera: Blackmagic Camera Control API manager class.
Part of the BMCCCamera library.
"""
import string
import random
import time

import requests
import urllib
from PyBMCC.BMCCAsyncApi import BMCCWebsocketState
from PyBMCC.BMCCTransport import BMCCTransport
from PyBMCC.BMCCLens import BMCCLens
from PyBMCC.BMCCSystem import BMCCSystem
from PyBMCC.BMCCEvent import BMCCEvent
from PyBMCC.BMCCTimeline import BMCCTimeline
from PyBMCC.BMCCVideo import BMCCVideo
from PyBMCC.BMCCAudio import BMCCAudio
from PyBMCC.BMCCMedia import BMCCMedia
from PyBMCC.BMCCColorCorrection import BMCCColorCorrection
from PyBMCC.BMCCPreset import BMCCPreset
import PyBMCC.Enums as Enums
import logging

class BMCCCamera:

    """Blackmagic Camera manager
    """

    host_or_ipaddr = None
    name = None
    atem_id = 0

    lens = None
    transport = None
    system = None
    event = None
    video = None
    audio = None
    media = None
    color_correction = None
    preset = None
    control_ATEM_ipaddr = None

    state = Enums.CameraState.UNKNOWN
    async_state = BMCCWebsocketState.INIT
    async_cam_state = {}
    state_update_timestamp = 0
    try_when_disconnected = False

    def __init__(self, host_or_ipaddr, camera_name=None, control_ATEM_ipaddr=None, try_when_disconnected = False):
        """Create BMCCCamera Camera Controller Object. This is the main class to control cameras

        :param str host_or_ipaddr: the host name or IP address of the camera to control  (required)
        :param str camera_name: the name to assign the camera (e.g. studio camera A). If unassigned, a random unique name
            will be generated  (optional)
        :param str control_ATEM_ipaddr: the host name or IP address of the ATEM switcher that will send camera
            commands via the SDI OUT/REF IN port. None if unspecified. (optional)
        :param bool try_when_disconnected: Automatically attempt to reconnect camera on next command if
            previous REST command failed. False if unspecified. (optional)

        """

        self.try_when_disconnected=try_when_disconnected
        self.host_or_ipaddr=host_or_ipaddr
        if camera_name is None:
            self.name = f"{host_or_ipaddr}"
        else:
            self.name = camera_name
        self.control_ATEM_ipaddr = control_ATEM_ipaddr
        self.lens = BMCCLens(self)
        self.transport = BMCCTransport(self)
        self.system = BMCCSystem(self)
        self.event = BMCCEvent(self)
        self.timeline = BMCCTimeline(self)
        self.video = BMCCVideo(self)
        self.audio = BMCCAudio(self)
        self.media = BMCCMedia(self)
        self.color_correction = BMCCColorCorrection(self)
        self.preset = BMCCPreset(self)
        self.update_state()
    def test_connection(self):
        try:
            url = f"http://{self.host_or_ipaddr}/control/documentation.html"
            r = requests.head(url,timeout=1)
            if r.status_code == 400:
                self.mark_connected()
            else:
                self.mark_disconnected()
        except requests.ConnectionError as ex:
            self.mark_disconnected()

    def handle_exception(self,ex,disconnect=True):
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logging.error(message)
        if disconnect:
            self.mark_disconnected()

    def mark_disconnected(self):
        self.state = Enums.CameraState.DISCONNECTED
        self.state_update_timestamp = time.time()

    def mark_connected(self):
        self.state = Enums.CameraState.CONNECTED
        self.state_update_timestamp = time.time()

    def update_state(self):
        self.test_connection()
        self.lens.get_iris()
        self.lens.get_zoom()
        self.lens.get_focus()
        self.transport.get_status()
        self.transport.get_record()
        self.system.get_supported_codec_formats()
        self.system.get_format()
        self.system.get_atem_id()
        self.audio.discover_channels()
        self.media.get_workingset()

    # convenience methods for BMCCLens
    def get_iris(self) -> float:
        return self.lens.get_iris()

    def set_iris(self, aperture_stop:float=None, normalised:float=None, aperture_number:int=None) -> int:
        return self.lens.set_iris(aperture_stop=aperture_stop, normalised=normalised, aperture_number=aperture_number)

    def get_zoom(self) -> float:
        return self.lens.get_zoom()

    def set_zoom(self, focal_length:float=None, normalised:float=None) -> int:
        return self.lens.set_zoom(focal_length=focal_length, normalised=normalised)

    def get_focus(self) -> float:
        return self.lens.get_focus()

    def set_focus(self, focus:float) -> int:
        return self.lens.set_focus(focus)

    def get_shutter(self) -> int:
        return self.video.get_shutter().shutter_speed

    def set_shutter(self,shutter_speed=None, shutter_angle=None) -> float:
        return self.video.set_shutter(shutter_speed=shutter_speed, shutter_angle=shutter_angle)

    def do_auto_focus(self) -> int:
        return self.lens.do_auto_focus()

    def record_start(self,clip_name:str=None) -> int:
        return self.transport.set_record(True,clip_name=clip_name)

    def record_stop(self) -> int:
        return self.transport.set_record(False)

    def get_timecode(self) -> str:
        return self.transport.get_timecode()

    def is_recording(self) -> bool:
        return self.transport.get_record()

    def get_last_clip_url(self,http_url=True,https_url=False,smb_url=False,smb_path=False) -> str:
        path=self.system.get_clips(only_last=True)
        if path==-1:
            return None
        if http_url:
            #return HTTP
            escaped_path=urllib.parse.quote(path, safe='/', encoding=None, errors=None)
            eps=escaped_path.split('/')
            # http://10.0.11.203/mounts/usb/X9%20Pro/1706224651.braw
            # http://10.0.11.203/mnt/usb16640/X9%20Pro/A010_02041219_C002.braw
            return f"http://{self.host_or_ipaddr}/mounts/usb/{eps[3]}/{eps[4]}"

def randomword(length:int) -> str:
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))
