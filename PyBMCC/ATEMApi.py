#!/usr/bin/env python3
# coding: utf-8

"""
ATEMApi: Blackmagic Camera Control ATEM API.
Part of the BMCCCamera library.
"""
import math

from fxpmath import Fxp
from PyATEMMax import ATEMMax
import logging

# ATEM CAMERA CONTROL, From the Blackmagic Design ATEM Camera Command SPEC 1.6.2
ATEM_CAMERA_DATATYPE_VOID = 0x00
ATEM_CAMERA_DATATYPE_VOID_LEN = 0
ATEM_CAMERA_DATATYPE_INT8 = 0x01
ATEM_CAMERA_DATATYPE_INT8_LEN = 1
ATEM_CAMERA_DATATYPE_INT16 = 0x02
ATEM_CAMERA_DATATYPE_INT16_LEN = 2
ATEM_CAMERA_DATATYPE_INT32 = 0x03
ATEM_CAMERA_DATATYPE_INT32_LEN = 4
ATEM_CAMERA_DATATYPE_INT64 = 0x04
ATEM_CAMERA_DATATYPE_INT64_LEN = 8
ATEM_CAMERA_DATATYPE_STRING = 0x05
ATEM_CAMERA_DATATYPE_STRING_LEN = 1
ATEM_CAMERA_DATATYPE_FIXED16 = 0x80
ATEM_CAMERA_DATATYPE_FIXED16_LEN = 2

ATEM_CAMERA_PACKET_BUFFER_SIZE=24
ATEM_CAMERA_PACKET_DEST = 0
ATEM_CAMERA_PACKET_CATEGORY = 1
ATEM_CAMERA_PACKET_PARAMETER = 2
ATEM_CAMERA_PACKET_TYPE = 4
ATEM_CAMERA_PACKET_COUNT = 7
ATEM_CAMERA_PACKET_COUNT_PROXY = 9
ATEM_CAMERA_PACKET_DATA = 16

ALL_CAMERAS = 255
class ATEMApi(ATEMMax):

    atem_ipaddr: str = None
    atem_auto_reconnect: bool = False
    def __init__(self,atem_ipaddr:str,autoconnect=True,atem_auto_reconnect=False):
        super().__init__()
        self.atem_ipaddr = atem_ipaddr
        self.atem_auto_reconnect = atem_auto_reconnect
        if(autoconnect):
            self.atem_connect()

    def atem_connect(self):
        logging.debug(f"Connecting to ATEM {self.atem_ipaddr}...")
        self.connect(self.atem_ipaddr)
        self.waitForConnection(infinite=False, timeout=1.0)

    def atem_disconnect(self):
        self.disconnect()
        self.atem_connected = False



    def atem_camera_command_pre(self) -> bool:
        if not self.connected:
            if not self.atem_auto_reconnect:
                return 1
            self.atem_connect()
            if self.connected:
                return 0
            return 1
        return 0

    def atem_get_camera_packet_size(self):
        return
    def atem_send_camera_command(self,
                                 destination_device: int,
                                 group_id: int,
                                 parameter_id: int,
                                 parameter_type: int,
                                 command_data_elements: int,
                                 command_data_signed: bool,
                                 command_data):

        self.switcher._prepareCommandPacket("CCmd", ATEM_CAMERA_PACKET_BUFFER_SIZE)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_DEST, destination_device)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_CATEGORY, group_id)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_PARAMETER, parameter_id)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_TYPE, parameter_type)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_COUNT, command_data_elements)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_COUNT_PROXY, command_data_elements)
        offset = ATEM_CAMERA_PACKET_DATA

        if parameter_type == ATEM_CAMERA_DATATYPE_STRING:
            self.switcher._outBuf.setString(offset,command_data_elements,command_data)
        else:
            for i in range(0,command_data_elements):
                if parameter_type==ATEM_CAMERA_DATATYPE_VOID:
                    pass
                elif parameter_type==ATEM_CAMERA_DATATYPE_INT8:
                    offset=offset+ATEM_CAMERA_DATATYPE_INT8_LEN
                    if command_data_signed:
                        self.switcher._outBuf.setU8(offset, command_data[i])
                    else:
                        self.switcher._outBuf.setS8(offset, command_data[i])
                elif parameter_type==ATEM_CAMERA_DATATYPE_INT16:
                    offset=offset+ATEM_CAMERA_DATATYPE_INT16_LEN
                    if command_data_signed:
                        self.switcher._outBuf.setU16(offset, command_data[i])
                    else:
                        self.switcher._outBuf.setS16(offset, command_data[i])
                elif parameter_type==ATEM_CAMERA_DATATYPE_INT32:
                    offset=offset+ATEM_CAMERA_DATATYPE_INT32_LEN
                    if command_data_signed:
                        self.switcher._outBuf.setU32(offset, command_data[i])
                    else:
                        self.switcher._outBuf.setS32(offset, command_data[i])
                elif parameter_type==ATEM_CAMERA_DATATYPE_INT64:
                    offset=offset+ATEM_CAMERA_DATATYPE_INT64_LEN
                    if command_data_signed:
                        self.switcher._outBuf.setU64(offset, command_data[i])
                    else:
                        self.switcher._outBuf.setS64(offset, command_data[i])
                elif parameter_type==ATEM_CAMERA_DATATYPE_FIXED16:
                    offset=offset+ATEM_CAMERA_DATATYPE_FIXED16_LEN
                    self.switcher._outBuf.setU16(offset, command_data[i])
                else:
                    raise Exception(f"{parameter_type} is not a known parameter type")

        self.switcher._finishCommandPacket()

        return

    def atem_camera_command_post(self):
        return
    
    # group 0 Lens
    # 0.0 Focus
    def setCameraLensFocus(self,destination_device:int=ALL_CAMERAS, focus:float=0.0) -> int:
        """Set Camera Control Focus

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:float focus (float): 0.0 = near , 1.0 = far

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=0,
            parameter_type=ATEM_CAMERA_DATATYPE_FIXED16,
            command_data_elements=1,
            command_data_signed=True,
            command_data=[getAtemFixed16(focus)])

        self.atem_camera_command_post()
        return 0

    # 0.1 Autofocus
    def setCameraLensAutofocus(self,destination_device:int=ALL_CAMERAS) -> int:
        """Set Camera Control Autofocus

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=1,
            parameter_type=ATEM_CAMERA_DATATYPE_VOID,
            command_data_elements=0,
            command_data_signed=True,
            command_data=None)

        self.atem_camera_command_post()
        return 0

    # 0.2 Aperture
    def setCameraLensAperture(self,destination_device:int=ALL_CAMERAS, fstop:float=4.0) -> int:
        """Set Camera Control Aperture

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:float fstop (float): desired f-stop. Camera will adjust to aperture nearest to provided value

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=2,
            parameter_type=ATEM_CAMERA_DATATYPE_FIXED16,
            command_data_elements=1,
            command_data_signed=True,
            command_data=[getAtemFixed16(math.sqrt(math.pow(2,fstop)))])

        self.atem_camera_command_post()
        return 0

def getAtemFixed16(val:float=0.0):
    fixed16 = Fxp(val, signed=True, n_word=16, n_frac=11)
    fixed16.rounding = 'around'
    return fixed16.val
