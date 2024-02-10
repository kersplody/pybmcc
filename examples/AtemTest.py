from PyBMCC.ATEMApi import ATEMApi,ALL_CAMERAS
import time

atem=ATEMApi("10.0.11.200")
print(atem.setCameraLensFocus(destination_device=ALL_CAMERAS,focus=1.0))
time.sleep(1)
print(atem.setCameraLensAutofocus())
atem.disconnect()
