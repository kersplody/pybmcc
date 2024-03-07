#!/usr/bin/env python3
# coding: utf-8

"""
ATEMApi: Blackmagic Camera Control ATEM API.
Part of the BMCCCamera library.
"""
import math
from enum import IntEnum
from socket import socket, AF_INET, SOCK_STREAM

from fxpmath import Fxp
from PyATEMMax import ATEMMax
import logging

# ATEM CAMERA CONTROL, From the Blackmagic Design ATEM Camera Command SPEC 1.6.2
ATEM_CAMERA_DATATYPE_VOID = 0x00
ATEM_CAMERA_DATATYPE_VOID_LEN = 0
ATEM_CAMERA_DATATYPE_BOOL = 0x00
ATEM_CAMERA_DATATYPE_BOOL_LEN = 0  # arrays of bool are not valid
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
ATEM_CAMERA_PACKET_COUNT_8 = 7
ATEM_CAMERA_PACKET_COUNT_16 = 9
ATEM_CAMERA_PACKET_COUNT_32 = 11
ATEM_CAMERA_PACKET_COUNT_64 = 13
ATEM_CAMERA_PACKET_DATA = 16

ALL_CAMERAS = 255

class BMCCAtemState(IntEnum):
    INIT = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTING = 3
    DISCONNECTED = 4
    CLOSED = 5
    DISABLED = 6

class ATEM(ATEMMax):

    atem_ipaddr: str = None
    atem_auto_reconnect: bool = False
    state = BMCCAtemState.INIT

    def __init__(self,atem_ipaddr:str,autoconnect=True,atem_auto_reconnect=False):
        super().__init__()
        self.atem_ipaddr = atem_ipaddr
        self.atem_auto_reconnect = atem_auto_reconnect
        if(autoconnect):
            self.atem_connect()

    def atem_connect(self) -> bool:
        logging.debug(f"Connecting to ATEM {self.atem_ipaddr}...")
        self.state=state = BMCCAtemState.CONNECTING

        #check for a route to host before connection attempt
        try:
            testSocket = socket(AF_INET, SOCK_STREAM)
            testSocket.settimeout(1)
            testSocket.connect((self.atem_ipaddr, 9994))
            testSocket.detach()
        except OSError as error:
            logging.error(f"atem: can't connect to {self.atem_ipaddr}: {error}")
            self.state = state = BMCCAtemState.DISCONNECTED
            return False

        self.connect(self.atem_ipaddr)
        connected=self.waitForConnection(infinite=False, timeout=1.0)
        if connected:
            self.state = BMCCAtemState.CONNECTED
        else:
            self.state = BMCCAtemState.DISCONNECTED
        return connected

    def atem_disconnect(self):
        self.disconnect()
        self.state = BMCCAtemState.DISCONNECTED

    def atem_camera_command_pre(self) -> bool:
        if not self.state == BMCCAtemState.CONNECTED:
            if not self.atem_auto_reconnect:
                return True
            self.atem_connect()
            if self.state == BMCCAtemState.CONNECTED:
                return False
            return True
        return False

    def atem_send_camera_command(self,
                                 destination_device: int,
                                 group_id: int,
                                 parameter_id: int,
                                 parameter_type: int,
                                 command_data_elements: int,
                                 command_data):

        self.switcher._prepareCommandPacket("CCmd", ATEM_CAMERA_PACKET_BUFFER_SIZE)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_DEST, destination_device)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_CATEGORY, group_id)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_PARAMETER, parameter_id)
        self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_TYPE, parameter_type)
        if parameter_type==ATEM_CAMERA_DATATYPE_INT32:
            self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_COUNT_32, command_data_elements)
        elif parameter_type == ATEM_CAMERA_DATATYPE_INT64:
            self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_COUNT_64, command_data_elements)
        elif parameter_type==ATEM_CAMERA_DATATYPE_INT8:
            self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_COUNT_8, command_data_elements)
        else:
            self.switcher._outBuf.setU8(ATEM_CAMERA_PACKET_COUNT_16, command_data_elements)
        offset = ATEM_CAMERA_PACKET_DATA

        if parameter_type == ATEM_CAMERA_DATATYPE_STRING:
            self.switcher._outBuf.setString(offset,command_data_elements,command_data)
        else:
            for i in range(0,command_data_elements):
                if parameter_type==ATEM_CAMERA_DATATYPE_VOID:
                    pass
                elif parameter_type==ATEM_CAMERA_DATATYPE_INT8:
                    self.switcher._outBuf.setU8(offset, command_data[i])
                    offset=offset+ATEM_CAMERA_DATATYPE_INT8_LEN
                elif parameter_type==ATEM_CAMERA_DATATYPE_INT16:
                    self.switcher._outBuf.setU16(offset, command_data[i])
                    offset=offset+ATEM_CAMERA_DATATYPE_INT16_LEN
                elif parameter_type==ATEM_CAMERA_DATATYPE_INT32:
                    self.switcher._outBuf.setU32(offset, command_data[i])
                    offset=offset+ATEM_CAMERA_DATATYPE_INT32_LEN
                elif parameter_type==ATEM_CAMERA_DATATYPE_INT64:
                    self.switcher._outBuf.setU64(offset, command_data[i])
                    offset=offset+ATEM_CAMERA_DATATYPE_INT64_LEN
                elif parameter_type==ATEM_CAMERA_DATATYPE_FIXED16:
                    self.switcher._outBuf.setU16(offset, command_data[i])
                    offset=offset+ATEM_CAMERA_DATATYPE_FIXED16_LEN
                else:
                    raise Exception(f"{parameter_type} is not a known parameter type")

        self.switcher._finishCommandPacket()

        return

    def atem_camera_command_post(self):
        return

    #########################################################################################
    # group 0 Lens
    #########################################################################################

    # 0.0 Focus
    def set_camera_lens_focus(self,destination_device:int=ALL_CAMERAS, focus:float=0.0) -> int:
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
            command_data=[get_atem_fixed16(check_range(focus,0.0,1.0,"LensFocus"))])

        self.atem_camera_command_post()
        return 0

    # 0.1 Autofocus
    def do_camera_lens_autofocus(self,destination_device:int=ALL_CAMERAS) -> int:
        """Do Camera Control Autofocus

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
            command_data=None)

        self.atem_camera_command_post()
        return 0

    # 0.2 Aperture
    def set_camera_lens_aperture(self,destination_device:int=ALL_CAMERAS, fstop:float=4.0) -> int:
        """Set Camera Control Aperture

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:float fstop (float): desired f-stop. Camera will adjust to aperture nearest to provided value

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        scaled_fstop=math.log(math.pow(fstop,2))/math.log(2)

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=2,
            parameter_type=ATEM_CAMERA_DATATYPE_FIXED16,
            command_data_elements=1,
            command_data=[get_atem_fixed16(scaled_fstop)])

        self.atem_camera_command_post()
        return 0

    # 0.3 Aperture Normalized
    def set_camera_lens_aperture_normalized(self,destination_device:int=ALL_CAMERAS, iris:float=0.0) -> int:
        """Set Camera Control Aperture Normalized

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:float fstop (float): desired f-stop. 0.0 = closed  1.0 = open

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=3,
            parameter_type=ATEM_CAMERA_DATATYPE_FIXED16,
            command_data_elements=1,
            command_data=[get_atem_fixed16(check_range(iris,0.0,1.0,"LensApertureNormalized"))])

        self.atem_camera_command_post()
        return 0

    # 0.4 Aperture Ordinal
    def set_camera_lens_aperture_ordinal(self,destination_device:int=ALL_CAMERAS, fstop_step:int=0) -> int:
        """Set Camera Control Aperture Step

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:int fstop_step (int): desired f-stop step. 0=closed/smallest

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=4,
            parameter_type=ATEM_CAMERA_DATATYPE_INT16,
            command_data_elements=1,
            command_data=[fstop_step])

        self.atem_camera_command_post()
        return 0

    # 0.5 Auto Aperture
    def set_camera_lens_auto_aperture(self,destination_device:int=ALL_CAMERAS) -> int:
        """Do Camera Auto Aperture

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=5,
            parameter_type=ATEM_CAMERA_DATATYPE_VOID,
            command_data_elements=0,
            command_data=None)

        self.atem_camera_command_post()
        return 0

    # 0.6 OIS
    def set_camera_lens_o_i_s(self,destination_device:int=ALL_CAMERAS, ois_enabled:bool=False) -> int:
        """Set Camera Lens OIS (Optical Image Stabilization) Enabled

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:bool ois_enabled: True=Enable False=Disable

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=6,
            parameter_type=ATEM_CAMERA_DATATYPE_BOOL,
            command_data_elements=1,
            command_data=[int(ois_enabled)])

        self.atem_camera_command_post()
        return 0

    # 0.7 Zoom Absolute
    def set_camera_lens_absolute_zoom(self, destination_device: int = ALL_CAMERAS, zoom_mm: int = 0) -> int:
        """Set Camera Zoom Absolute

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:int zoom_mm (int): lens value to zoom to in millimeters

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=7,
            parameter_type=ATEM_CAMERA_DATATYPE_INT16,
            command_data_elements=1,
            command_data=[zoom_mm])

        self.atem_camera_command_post()
        return 0

    # 0.8 Zoom Normalized
    def set_camera_lens_zoom_normalized(self, destination_device: int = ALL_CAMERAS, zoom: float = 0.0) -> int:
        """Set Camera Control Aperture Normalized

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:float zoom (float): desired zoom level. 0.0 = wide  1.0 = narrow/zoomed

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=8,
            parameter_type=ATEM_CAMERA_DATATYPE_FIXED16,
            command_data_elements=1,
            command_data=[get_atem_fixed16(check_range(zoom, 0.0, 1.0, "LensZoomNormalized"))])

        self.atem_camera_command_post()
        return 0

    # 0.9 Continuous Zoom Speed
    def set_camera_lens_zoom_continuous_speed(self, destination_device: int = ALL_CAMERAS, zoom_speed: float = 0.0) -> int:
        """Set Camera Control Aperture Normalized

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:float zoom_speed (float): desired zoom level. -1.0 = wide fast, 0.0 =  stopped, 1.0 = tele fast

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=0,
            parameter_id=9,
            parameter_type=ATEM_CAMERA_DATATYPE_FIXED16,
            command_data_elements=1,
            command_data=[get_atem_fixed16(check_range(zoom_speed, -1.0, 1.0, "LensZoomContinuousSpeed"))])

        self.atem_camera_command_post()
        return 0

    #########################################################################################
    # group 1
    #########################################################################################

    # 1.5 Shutter Angle
    def set_camera_video_exposure(self, destination_device: int = ALL_CAMERAS, exposure_us: int = 16666) -> int:
        """Set Camera Control Aperture Normalized

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:int exposure_us (int): exposure time in microseconds (1-42000)

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=1,
            parameter_id=5,
            parameter_type=ATEM_CAMERA_DATATYPE_INT32,
            command_data_elements=1,
            command_data=[check_range(exposure_us, 1, 42000, "VideoExposure")])

        self.atem_camera_command_post()
        return 0

    # 1.11 Shutter Angle
    def set_camera_video_shutter_angle(self, destination_device: int = ALL_CAMERAS, angle: int = 360) -> int:
        """Set Camera Control Aperture Normalized

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:int angle (int): angle in degrees (0-360)

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=1,
            parameter_id=11,
            parameter_type=ATEM_CAMERA_DATATYPE_INT32,
            command_data_elements=1,
            command_data=[check_range(angle, 1, 360, "VideoShutterAngle")*100])

        self.atem_camera_command_post()
        return 0

    # 1.12 Shutter Speed

    def set_camera_video_shutter_speed(self, destination_device: int = ALL_CAMERAS, speed: int = 60) -> int:
        """Set Camera Control Aperture Normalized

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:int speed (int): shutted speed in fractions of a second (1/n)

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=1,
            parameter_id=12,
            parameter_type=ATEM_CAMERA_DATATYPE_INT32,
            command_data_elements=1,
            command_data=[check_range(speed, 0, 100000, "VideoShutterSpeed")])

        self.atem_camera_command_post()
        return 0

    #########################################################################################
    # group 3 Output
    #########################################################################################

    #3.0 Overlay Enables
    def set_camera_output_overlay_enables(self, destination_device: int = ALL_CAMERAS,
                                      status:bool=False,
                                      frame_guide:bool=False,
                                      clean_feed:bool=False,
                                      output_device:int = 2) -> int:
        """Set Camera Control Output Overlay (Not all cameras support all modes, overlays may not be available on all
        outputs)

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:bool status (bool): True=show status overlay. False by default.
        :param:bool frame_guide (bool): True=show frame_guide overlay. False by default.
        :param:bool clean_feed (bool): True=enable clean feed. False by default.
        :param:int output_device (int): bit field=> 0=LCD 1=HDMI 2=EVF 3=mainSDI 4=frontSDI

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        field1=int(clean_feed)*4+int(frame_guide)*2+int(status)

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=3,
            parameter_id=0,
            parameter_type=ATEM_CAMERA_DATATYPE_INT16,
            command_data_elements=2,
            command_data=[field1,output_device])

        self.atem_camera_command_post()
        return 0

    #########################################################################################
    # group 4 Display
    #########################################################################################

    #4.1
    def set_camera_display_exposure_tool(self, destination_device: int = ALL_CAMERAS,
                                      zebra:bool=False,
                                      focus_assist:bool=False,
                                      false_color:bool=False,
                                      output_device:int = 2) -> int:
        """Set Camera Control Output Overlay (Not all cameras support all modes, overlays may not be available on all
        outputs)

        :param:int camera_atem_id: Camera ATEM id. ALL_CAMERAS if unspecified (optional)
        :param:bool zebra (bool): True=enable zebra. False by default.
        :param:bool focus_assist (bool): True=enable focus_assist. False by default.
        :param:bool false_color (bool): True=enable false_color. False by default.
        :param:int output_device (int): bit field=> 0=LCD 1=HDMI 2=EVF 3=mainSDI 4=frontSDI

        :return: int: 0 on success, nonzero on failure
        """
        if self.atem_camera_command_pre():
            return 1

        field1=int(false_color)*4+int(focus_assist)*2+int(zebra)

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=4,
            parameter_id=1,
            parameter_type=ATEM_CAMERA_DATATYPE_INT16,
            command_data_elements=2,
            command_data=[field1,output_device])

        self.atem_camera_command_post()
        return 0

    #########################################################################################
    # group 10 Media
    #########################################################################################

    #10.1 Transport Mode
    def set_camera_media_mode(self, destination_device: int = ALL_CAMERAS,
                           mode:int=0,
                           speed:int=1,
                           flags:int=1<<5,
                           slot_1:int=1,
                           slot_2:int=1) -> int:

        if self.atem_camera_command_pre():
            return 1

        self.atem_send_camera_command(
            destination_device=destination_device,
            group_id=10,
            parameter_id=1,
            parameter_type=ATEM_CAMERA_DATATYPE_INT8,
            command_data_elements=5,
            command_data=[mode,speed,flags,slot_1,slot_2])

        self.atem_camera_command_post()
        return 0
    def set_camera_media_mode_record(self,destination_device: int = ALL_CAMERAS):
        self.set_camera_media_mode(destination_device=destination_device,mode=2)
    def set_camera_media_mode_idle(self,destination_device: int = ALL_CAMERAS):
        self.set_camera_media_mode(destination_device=destination_device,mode=0)

def get_atem_fixed16(val:float=0.0):
    fixed16 = Fxp(val, signed=True, n_word=16, n_frac=11)
    fixed16.rounding = 'around'

    return fixed16.val

def check_range(val,min,max,param):
    if val<min:
        logging.warning(f"Parameter {param} is outside of permissible range of (f{min} to f{max})")
        return min
    if val>max:
        logging.warning(f"Parameter {param} is outside of permissible range of (f{min} to f{max})")
        return max
    return val
