"""
Technisync Komodo Driver

(c) 2021 Kersplody Corporation
Author: Christopher Howard

"""
import json
from collections import OrderedDict

import websocket
from websocket._exceptions import WebSocketConnectionClosedException
import logging
import _thread
import time
import threading
from enum import IntEnum
from queue import Queue, Empty
from dataclasses import dataclass

messageCount = 0
gotMsgEvent = threading.Event()

class BMCCMessageType(IntEnum):
    CAMSTATE = 0,
    EVENT = 1

@dataclass
class BMCCMessage:
    src: str
    type: BMCCMessageType
    message: str
    ts: float = time.time()

class BMCCWebsocketState(IntEnum):
    INIT = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTING = 3
    DISCONNECTED = 4
    CLOSED = 5
    DISABLED = 6

class BMCCWebsocketClient:

    webSocketApp = None
    camera = None
    inputQueue: Queue = None
    outputQueue: Queue = None
    webSocketAddress: str
    autoRecover = True
    ws = None
    bmccWebsocketState = BMCCWebsocketState.INIT

    def close_connection(self, autoRecover=True):
        logging.info("ws: {} :DISCONNECTING {}".format(self.camera.name,self.webSocketAddress))
        self.bmccWebsocketState = BMCCWebsocketState.DISCONNECTING
        self.inputQueue.put(BMCCMessage(self.camera.name, BMCCMessageType.CAMSTATE, self.bmccWebsocketState.name))
        self.autoRecover = autoRecover
        self.ws.close()

    def on_message(self, ws, message):
        logging.debug("ws: {} :GOT_MSG {}".format(self.camera.name,message))
        self.inputQueue.put(BMCCMessage(self.camera.name, BMCCMessageType.EVENT, message))

    def on_error(self, ws, error):
        logging.error("ws: {} :GOT_ERR {}\r".format(self.camera.name,error))

    def on_close(self, ws, close_status_code, close_msg):
        # clear the queues
        with self.outputQueue.mutex:
            self.outputQueue.queue.clear()

        self.bmccWebsocketState = BMCCWebsocketState.CLOSED
        self.inputQueue.put(BMCCMessage(self.camera.name, BMCCMessageType.CAMSTATE, self.bmccWebsocketState.name))

        logging.debug("ws: {}  :CLOSED {}".format(self.camera.name,self.webSocketAddress))

    def on_open(self, ws):
        self.bmccWebsocketState = BMCCWebsocketState.CONNECTED
        self.inputQueue.put(BMCCMessage(self.camera.name, BMCCMessageType.CAMSTATE, self.bmccWebsocketState.name))
        logging.info("ws: {} :CONNECTED {}".format(self.camera.name,self.webSocketAddress))

        # clear the queues
        with self.outputQueue.mutex:
            self.outputQueue.queue.clear()

        # configure the connection
        try:
            time.sleep(.1)
            # send init message
            json_out = getSubscribeAllMessage()
            logging.debug("ws: {} :SND_MSG {}".format(self.camera.name,json_out))
            ws.send(json_out)
            time.sleep(.1)
            # unsubscribe timecode
            json_out = getUnsubscribeChannelMessage()
            logging.debug("ws: {}  :SND_MSG {}".format(self.camera.name,json_out))
            ws.send(json_out)
        except WebSocketConnectionClosedException:
            self.close_connection()
            return

        def run(*args):
            while True:
                json_out = self.outputQueue.get()
                if json_out is None:
                    self.close_connection(False)
                    return
                logging.debug("ws: {} :SND_MSG {}".format(self.camera.name,json_out))
                try:
                    ws.send(json_out)
                except WebSocketConnectionClosedException:
                    logging.debug("ws: {} WebSocketConnectionClosedException".format(self.camera.name))
                    self.close_connection()
                    return
                time.sleep(.01)

        _thread.start_new_thread(run, ())

    def __init__(self, dataQueueIn: Queue, dataQueueOut: Queue, camera , enableTrace=False, autoRecover=True,
                 pingInterval=15, pingTimeout=1):
        websocket.enableTrace(enableTrace)
        websocket.setdefaulttimeout(1)
        self.inputQueue = dataQueueIn
        self.outputQueue = dataQueueOut
        self.autoRecover = autoRecover
        self.camera = camera
        self.webSocketAddress = f"ws://{camera.host_or_ipaddr}/control/api/v1/event/websocket"
        self.connect()

    def connect(self):
        while self.autoRecover:
            self.bmccWebsocketState = BMCCWebsocketState.CONNECTING
            self.inputQueue.put(
                BMCCMessage(self.camera.name, BMCCMessageType.CAMSTATE, self.bmccWebsocketState.name))
            logging.debug("ws: {} :CONNECT ".format(self.camera.name))
            self.ws = websocket.WebSocketApp(self.webSocketAddress,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close)
            self.ws.run_forever(ping_interval=15, ping_timeout=1)
            self.bmccWebsocketState = BMCCWebsocketState.DISCONNECTED
            self.inputQueue.put(
                BMCCMessage(self.camera.name, BMCCMessageType.CAMSTATE, self.bmccWebsocketState.name))

            if self.autoRecover:
                time.sleep(5)
                while not self.outputQueue.empty():
                    if self.outputQueue.get() is None:
                        self.autoRecover = False
                if self.autoRecover:
                    logging.debug("ws: {} :RECONNECT".format(self.camera.name))

class AsyncMessageProcessor:

    camera = None

    def __init__(self, camera):
        self.camera=camera
    def process_property(self, property, value):

        if type(value) is OrderedDict:
            value=dict(value)
        else:
            v={}
            v["state"]=value
            value=v
        value['ts']=time.time()

        self.camera.async_cam_state[property] = value
        if property in self.camera.async_cam_state:
            self.camera.async_cam_state[property]=value
            logging.debug(f"process_property: Updating {property} -> {value}")
            return
        logging.debug(f"process_property: Setting {property} -> {value}")

    def process_message(self, message: BMCCMessage):
        if not message:
            logging.debug("Got None message")
        else:
            logging.debug("Processing " + str(message.message))
        if message.type == BMCCMessageType.CAMSTATE:
            self.camera.async_state = message.message
            logging.debug(
                "process_async_message CAMSTATE: CAM " + message.src + " State changed to: " + str(message.message))
            return
        m = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(message.message)
        if 'type' not in m:
            logging.warning(
                f"process_async_message ???: Response missing type field. MESSAGE: {message.message}")
            return
        if m['type'] == 'response':
            logging.debug(
                f"process_async_message response: MESSAGE: {message.message}")
            if m['data']["action"] == "subscribe":
                for key, value in m['data']['values'].items():
                    self.process_property(key, value)
            return
        elif m['type'] != 'event':
            logging.debug(
                f"process_async_message ???: No handler for {m['type']} message type. MESSAGE: {message.message}")
            return
        if 'data' not in m:
            logging.warning(
                f"process_async_message ???: Response missing data field. MESSAGE: {message.message}")
            return
        if 'action' not in m['data']:
            logging.warning(
                f"process_async_message ???: Response missing data.action field. MESSAGE: {message.message}")
            return
        if m['data']['action'] != 'propertyValueChanged':
            logging.debug(
                "process_async_message EVENT: CAM " + message.src + " EVENT: " + str(m['data']['action']))
            return
        if 'property' not in m['data']:
            logging.warning(
                f"process_async_message EVENT: Response missing data.action.property field. MESSAGE: {message.message}")
            return
        if 'value' not in m['data']:
            logging.warning(
                f"process_async_message EVENT: Response missing data.action.value field. MESSAGE: {message.message}")
            return
        logging.debug(
            f"process_async_message EVENT: CAM {message.src} EVENT: {m['data']['action']} {m['data']['property']}:{m['data']['value']}")
        self.process_property(m['data']['property'], m['data']['value'])

def getSubscribeAllMessage() -> str:
    return '{"data": {"action": "subscribe", "properties": ["*"]}, "type": "request"}'
def getUnsubscribeChannelMessage(channel="/transports/0/timecode") -> str:
    return '{"data": {"action": "unsubscribe", "properties": ["'+str(channel)+'"]}, "type": "request"}'
