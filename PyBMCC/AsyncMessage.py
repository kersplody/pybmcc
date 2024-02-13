#!/usr/bin/env python3
# coding: utf-8
import time
from dataclasses import dataclass
from enum import IntEnum, auto


class BMCCMessageType(IntEnum):
    CAMSTATE = 0,
    EVENT = 1,
    JSON = 2,
    ATEM = 3,
    REST = 4


class BMCCConnectionState(IntEnum):
    INIT = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTING = 3
    DISCONNECTED = 4
    CLOSED = 5
    DISABLED = 6


class BMCCMessageCommands(IntEnum):
    # ATEM COMMANDS
    set_camera_output_overlay_enables = auto()
    set_camera_display_exposure_tool = auto()
    set_camera_lens_auto_aperture = auto()
    set_camera_lens_zoom_continuous_speed = auto()
    set_camera_lens_focus = auto()
    do_camera_lens_autofocus = auto()
    set_camera_lens_aperture = auto()
    set_camera_lens_aperture_normalized = auto()
    set_camera_lens_aperture_ordinal = auto()
    set_camera_lens_ois = auto()
    set_camera_lens_absolute_zoom = auto()
    set_camera_lens_zoom_normalized = auto()
    set_camera_video_exposure = auto()
    set_camera_video_shutter_angle = auto()
    set_camera_video_shutter_speed = auto()
    set_camera_media_mode = auto()
    set_camera_media_mode_record = auto()
    set_camera_media_mode_idle = auto()

    # REST COMMANDS
    get_camera_audio_discover_channels = auto()
    get_camera_audio_channel_input = auto()
    set_camera_audio_channel_input = auto()
    get_camera_audio_channel_input_description = auto()
    get_camera_audio_channel_input_supported_inputs = auto()
    get_camera_audio_channel_input_level = auto()
    set_camera_audio_channel_input_level = auto()
    get_camera_audio_channel_phantom_power = auto()
    set_camera_audio_channel_phantom_power = auto()
    get_camera_audio_channel_padding = auto()
    set_camera_audio_channel_padding = auto()
    get_camera_audio_channel_low_cut_filter = auto()
    set_camera_audio_channel_low_cut_filter = auto()
    get_camera_audio_channel_available = auto()
    get_camera_color_lift = auto()
    set_camera_color_lift = auto()
    get_camera_color_gamma = auto()
    set_camera_color_gamma = auto()
    get_camera_color_gain = auto()
    set_camera_color_gain = auto()
    get_camera_color_offset = auto()
    set_camera_color_offset = auto()
    get_camera_color_contrast = auto()
    set_camera_color_contrast = auto()
    get_camera_color_color = auto()
    set_camera_color_color = auto()
    get_camera_color_luma_contribution = auto()
    set_camera_color_luma_contribution = auto()
    get_camera_events_events = auto()
    get_camera_lens_iris_stops = auto()
    get_camera_lens_aperture_stops = auto()
    get_camera_lens_iris = auto()
    set_camera_lens_iris = auto()
    # set_camera_lens_aperture = auto()  # overlap with ATEM
    get_camera_lens_aperture = auto()
    get_camera_lens_zoom = auto()
    set_camera_lens_zoom = auto()
    get_camera_lens_focus = auto()
    # set_camera_lens_focus = auto()  # overlap with ATEM
    # do_camera_lens_autofocus = auto()  # overlap with ATEM
    get_camera_media_workingset = auto()
    get_camera_media_active = auto()
    set_camera_media_active = auto()
    get_camera_media_supported_filesystems = auto()
    get_camera_media_device_info = auto()
    get_camera_media_device_format_key = auto()
    do_camera_media_do_device_format = auto()
    set_camera_preset_get_presets = auto()
    do_camera_preset_upload_preset = auto()
    get_active_preset = auto()
    set_active_preset = auto()
    do_camera_preset_download_preset = auto()
    do_camera_preset_overwrite_preset = auto()
    do_camera_preset_delete_preset = auto()
    get_camera_system_system = auto()
    get_camera_system_supported_codec_formats = auto()
    get_camera_system_codec_format = auto()
    set_camera_system_codec_format = auto()
    get_camera_system_video_format = auto()
    set_camera_system_video_format = auto()
    get_camera_system_supported_video_formats = auto()
    get_camera_system_format = auto()
    set_camera_system_format = auto()
    get_camera_system_atem_id = auto()
    set_camera_system_atem_id = auto()
    get_camera_system_clips = auto()
    get_camera_timeline_timeline = auto()
    do_camera_timeline_append_timeline = auto()
    do_camera_timeline_delete_timeline = auto()
    get_camera_transport_status = auto()
    set_camera_transport_status = auto()
    get_camera_transport_stop = auto()
    set_camera_transport_stop = auto()
    get_camera_transport_play = auto()
    set_camera_transport_play = auto()
    get_camera_transport_playback = auto()
    set_camera_transport_playback = auto()
    get_camera_transport_record = auto()
    set_camera_transport_record = auto()
    get_camera_transport_timecode = auto()
    get_camera_transport_timecode_source = auto()
    get_camera_video_iso = auto()
    set_camera_video_iso = auto()
    get_camera_video_gain = auto()
    set_camera_video_gain = auto()
    get_camera_video_white_balance = auto()
    set_camera_video_white_balance = auto()
    do_camera_video_do_auto_white_balance = auto()
    get_camera_video_white_balance_tint = auto()
    set_camera_video_white_balance_tint = auto()
    get_camera_video_nd_filter = auto()
    set_camera_video_nd_filter = auto()
    get_camera_video_nd_filter_display_mode = auto()
    set_camera_video_nd_filter_display_mode = auto()
    get_camera_video_shutter = auto()
    set_camera_video_shutter = auto()
    get_camera_video_auto_exposure = auto()
    put_camera_video_auto_exposure = auto()

@dataclass
class BMCCMessage:
    src: str
    type: BMCCMessageType
    message: str = None
    command: BMCCMessageCommands = None
    args: dict = None
    delay: float = 0.0
    ts: float = time.time()
