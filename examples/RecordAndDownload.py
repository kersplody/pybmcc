from PyBMCC import BMCCCamera
from PyBMCC.Enums import CameraState
import time

camera = BMCCCamera("10.0.11.203")
if camera.state != CameraState.CONNECTED:
    print("Camera Not connected")
    exit(1)
camera.set_iris(aperture_stop=8.0)   #f8
camera.set_zoom(focal_length=25)     #25mm
camera.set_shutter(shutter_angle=180) #180° Shutter
camera.do_auto_focus()
time.sleep(1.0) # Wait for the lens
camera.record_start()
time.sleep(3.0) # 3 second clip
camera.record_stop()
print(camera.get_last_clip_url())

