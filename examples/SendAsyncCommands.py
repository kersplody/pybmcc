from PyBMCC import AsyncMessageProcessor, BMCCMessage, BMCCMessageCommands, BMCCMessageType, ATEM, BMCCCamera
from queue import Queue, Empty
import time
import logging


logging.basicConfig(level=logging.DEBUG)
command_queue = Queue()
src="test_driver"
type=BMCCMessageType.ATEM
atem=ATEM(atem_ipaddr="10.0.11.200")
mp = AsyncMessageProcessor(camera=None,atem=atem,command_queue=command_queue)
mp.start_command_queue_processing()

command_queue.put(BMCCMessage(src=src,type=type,command=BMCCMessageCommands.get_camera_color_lift,delay=1.0))
command_queue.put(BMCCMessage(src=src,type=type,command=BMCCMessageCommands.do_camera_lens_autofocus,delay=1.0))
command_queue.put(BMCCMessage(src=src,type=type,command=BMCCMessageCommands.set_camera_lens_aperture,args={'fstop':2.0},delay=1.0))
command_queue.put(BMCCMessage(src=src,type=type,command=BMCCMessageCommands.set_camera_video_shutter_angle,args={'angle':360},delay=1.0))
command_queue.put(None)
time.sleep(1)
while mp.command_queue_thread_running:
    time.sleep(1)
atem.disconnect()

type = BMCCMessageType.REST
mp = AsyncMessageProcessor(camera=BMCCCamera("10.0.11.203"),atem=None,command_queue=command_queue)
mp.start_command_queue_processing()

command_queue.put(BMCCMessage(src=src,type=type,command=BMCCMessageCommands.get_camera_color_lift))
command_queue.put(BMCCMessage(src=src,type=type,command=BMCCMessageCommands.do_camera_lens_autofocus,delay=1.0))
command_queue.put(BMCCMessage(src=src,type=type,command=BMCCMessageCommands.get_camera_lens_aperture_stops,delay=10.0))
command_queue.put(BMCCMessage(src=src,type=type,command=BMCCMessageCommands.set_camera_lens_aperture,args={'fstop':2.6}))

while mp.command_queue_thread_running:
    time.sleep(1)


