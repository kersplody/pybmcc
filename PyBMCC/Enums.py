#!/usr/bin/env python3
# coding: utf-8

from enum import Enum

UNKNOWN='UNKNOWN'

class CameraState(Enum):
    UNKNOWN = 1
    DISCONNECTED = 2
    CONNECTED = 3
