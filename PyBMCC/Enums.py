#!/usr/bin/env python3
# coding: utf-8

from enum import Enum

UNKNOWN='UNKNOWN'

class CameraState(Enum):
    UNKNOWN = 1
    DISCONNECTED = 2
    CONNECTED = 3

class CommandStauts(Enum):
    SUCCESS = 0
    REST_ERROR = -1
    CAM_DISCONNECTED = -2
    BAD_ARGS = -3
    NOT_IMPLEMENTED_ON_CAMERA = -4

class TransportStatus(Enum):
    UNKNOWN = -1
    PASSTHROUGH = 0
    STOP = 1
    PLAY = 2
    RECORD = 3
class TransportResponse(Enum):
    UNKNOWN = -1
    InputPreview = 0
    InputRecord = 1
    Output = 2

class TransportPlayback(Enum):
    UNKNOWN = -1
    Play = 0
    Jog = 1
    Shuttle = 2
    Var = 3

class TimecodeSource(Enum):
    UNKNOWN = 0
    Timecode = 1
    Clip = 2
