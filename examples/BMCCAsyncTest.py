import logging
import _thread
import time
from queue import Queue, Empty
from PyBMCC.BMCCCamera import BMCCCamera
from PyBMCC.AsyncApi import BMCCWebsocketClient,AsyncMessageProcessor

if __name__ == "__main__":

    dataQueueIn = Queue()
    dataQueueOut = Queue()

    logging.basicConfig(level=logging.DEBUG)
    camera=BMCCCamera("10.0.11.203")
    _thread.start_new_thread(BMCCWebsocketClient, (dataQueueIn, dataQueueOut, camera, False))
    mp=AsyncMessageProcessor(camera)

    for x in range(50):  #die after 50 messages
        try:
            message = dataQueueIn.get(timeout=5)
            mp.process_message(message)
            while not dataQueueIn.empty():
                message = dataQueueIn.get(timeout=5)
                mp.process_message(message)

        except Empty:
            logging.debug("No camera messages in last 5 seconds")
        time.sleep(3)

    dataQueueOut.put(None)
    time.sleep(3)
    try:
        message = dataQueueIn.get(timeout=5)
        mp.process_message(message)
        while not dataQueueIn.empty():
            message = dataQueueIn.get(timeout=5)
            mp.process_message(message)
    except Empty:
        logging.debug("No camera messages in last 5 seconds")
