#!/usr/bin/env python3
# coding: utf-8

import string
import random
import PyBMCC.BMCCLens as BMCCLens
import PyBMCC.Enums as Enums
import time
import requests

class BMCCCamera:
    host_or_ipaddr = None
    name = None
    atem_id = 0
    lens = None
    state = Enums.CameraState.UNKNOWN
    state_update_timestamp = 0

    def __init__(self, host_or_ipaddr, name=None, atem_id=1):
        self.host_or_ipaddr=host_or_ipaddr
        if name is None:
            name = randomword(8)
        self.name = name
        self.atem_id = atem_id
        self.lens=BMCCLens(self)
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
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))