from PyBMCC import ATEM, ALL_CAMERAS
import time

atem=ATEM("10.0.11.200")



#0.0
atem.set_camera_lens_focus(destination_device=4,focus=0.5)
time.sleep(1)
#0.1
atem.do_camera_lens_autofocus()
#0.2
atem.set_camera_lens_aperture(fstop=4.0)
time.sleep(1)
#0.3
atem.set_camera_lens_aperture_normalized(iris=0.25)
time.sleep(1)
#0.4
atem.set_camera_lens_aperture_ordinal(fstop_step=600)
time.sleep(1)
#0.5
atem.set_camera_lens_auto_aperture()
#1.5
atem.set_camera_video_exposure(exposure_us=int(1/1000*1000000))
#1.11
atem.set_camera_video_shutter_angle(angle=180)
#1.12
atem.set_camera_video_shutter_speed(speed=60)
#3.0
atem.set_camera_output_overlay_enables(clean_feed=True)
time.sleep(1)
atem.set_camera_output_overlay_enables(status=True)
#4.1
atem.set_camera_display_exposure_tool(false_color=True)
time.sleep(1)
atem.set_camera_display_exposure_tool(false_color=False)
#10.0
atem.set_camera_media_mode_record()
time.sleep(3)
atem.set_camera_media_mode_idle()
atem.disconnect()
