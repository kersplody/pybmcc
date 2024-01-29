#!/usr/bin/env python3
# coding: utf-8

import string
import random
import time
import requests
from PyBMCC.BMCCTransport import BMCCTransport
from PyBMCC.BMCCLens import BMCCLens
from PyBMCC.BMCCSystem import BMCCSystem
import PyBMCC.Enums as Enums
import logging

class BMCCCamera:
    host_or_ipaddr = None
    name = None
    atem_id = 0

    lens = None
    transport = None
    system = None

    state = Enums.CameraState.UNKNOWN
    state_update_timestamp = 0
    try_when_disconnected = False

    def __init__(self, host_or_ipaddr, name=None, atem_id=1):
        self.host_or_ipaddr=host_or_ipaddr
        if name is None:
            name = randomword(8)
        self.name = name
        self.atem_id = atem_id
        self.lens = BMCCLens(self)
        self.transport = BMCCTransport(self)
        self.system = BMCCSystem(self)
        self.update_state()
    def test_connection(self):
        try:
            r = requests.head(f"http://{self.host_or_ipaddr}/control/documentation.html")
            if r.status_code == 400:
                self.mark_connected()
            else:
                self.mark_disconnected()
        except requests.ConnectionError:
            self.mark_disconnected()

    def handle_exception(self,ex):
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logging.error(message)
        self.mark_disconnected()

    def mark_disconnected(self):
        self.state = Enums.CameraState.DISCONNECTED
        self.state_update_timestamp = time.time()

    def mark_connected(self):
        self.state = Enums.CameraState.CONNECTED
        self.state_update_timestamp = time.time()

    def update_state(self):
        self.test_connection()
        self.get_iris
        self.lens.get_zoom()
        self.lens.get_focus()
        self.transport.get_status()
        self.transport.get_record()
        self.system.get_supported_codec_formats()
        self.system.get_format()

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

def randomword(length:int) -> str:
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))