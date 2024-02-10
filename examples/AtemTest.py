from PyBMCC.ATEMApi import ATEMApi,ALL_CAMERAS
import time

atem=ATEMApi("10.0.11.200")

#0.0
#atem.setCameraLensFocus(destination_device=ALL_CAMERAS,focus=0.5)
#time.sleep(1)
#0.1
#atem.setCameraLensAutofocus()
#0.2
#atem.setCameraLensAperture(fstop=4.0)
#time.sleep(1)
#0.3
#atem.setCameraLensApertureNormalized(iris=0.25)
#time.sleep(1)
#0.4
#atem.setCameraLensApertureOrdinal(fstop_step=600)
#time.sleep(1)
#0.5
#atem.setCameraLensAutoAperture()
#1.5
#atem.setCameraVideoExposure(exposure_us=int(1/1000*1000000))
#1.11
#atem.setCameraVideoShutterAngle(angle=180)
#1.12
#atem.setCameraVideoShutterSpeed(speed=60)
#3.0
#atem.setCameraOutputOverlayEnables(status=True)
#4.1
#atem.setCameraDisplayExposureTool(false_color=False)
#10.0
atem.setCameraMediaModeRecord()
time.sleep(3)
atem.setCameraMediaModeIdle()
atem.disconnect()
