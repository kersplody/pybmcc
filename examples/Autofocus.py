#!/usr/bin/env python3
# coding: utf-8

from PyBMCC import BMCCLens
from PyBMCC import BMCCCamera
import logging
import time

logging.basicConfig(level=logging.DEBUG)

camera=BMCCCamera("10.0.11.203")

#FOCUS
print(camera.lens.get_focus())
camera.lens.set_focus(0.0)
time.sleep(1)
print(camera.lens.get_focus())
camera.lens.set_focus(1.0)
time.sleep(1)
print(camera.lens.get_focus())
camera.lens.do_auto_focus()
time.sleep(1.25)
print(camera.lens.get_focus())
exit(0)

#ZOOM
print(camera.lens.get_zoom())
camera.lens.set_zoom(normalised=.5)
time.sleep(.5)
print(camera.lens.get_zoom())

#IRIS
camera.lens.set_iris(8)
time.sleep(.5)
print(camera.lens.get_iris())
camera.lens.set_iris(normalised=1.0)
time.sleep(.5)
print(camera.lens.get_iris())
camera.lens.set_iris(normalised=0.0)
time.sleep(.5)
print(camera.lens.get_iris())

