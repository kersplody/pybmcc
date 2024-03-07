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
from queue import Queue
import re

from PyBMCC.AsyncMessage import BMCCConnectionState, BMCCMessage, BMCCMessageType, BMCCMessageCommands
from PyBMCC.AtemApi import BMCCAtemState, ATEM, ALL_CAMERAS

CC2SC = re.compile(r'(?<!^)(?=[A-Z])')

class BMCCWebsocketClient:

    webSocketApp = None
    camera = None
    inputQueue: Queue = None
    outputQueue: Queue = None
    webSocketAddress: str
    autoRecover = True
    ws = None
    BMCCConnectionState = BMCCConnectionState.INIT

    def get_camname(self):
        return self.camera.name if self.camera else "None"

    def close_connection(self, autoRecover=True):
        logging.info("ws: {} :DISCONNECTING {}".format(self.get_camname(),self.webSocketAddress))
        self.BMCCConnectionState = BMCCConnectionState.DISCONNECTING
        self.inputQueue.put(BMCCMessage(self.get_camname(), BMCCMessageType.CAMSTATE, self.BMCCConnectionState.name))
        self.autoRecover = autoRecover
        self.ws.close()

    def on_message(self, ws, message):
        logging.debug("ws: {} :GOT_MSG {}".format(self.get_camname(),message))
        self.inputQueue.put(BMCCMessage(self.get_camname(), BMCCMessageType.EVENT, message))

    def on_error(self, ws, error):
        logging.error("ws: {} :GOT_ERR {}\r".format(self.get_camname(),error))

    def on_close(self, ws, close_status_code, close_msg):
        # clear the queues
        with self.outputQueue.mutex:
            self.outputQueue.queue.clear()

        self.BMCCConnectionState = BMCCConnectionState.CLOSED
        self.inputQueue.put(BMCCMessage(self.get_camname(), BMCCMessageType.CAMSTATE, self.BMCCConnectionState.name))

        logging.debug("ws: {}  :CLOSED {}".format(self.get_camname(),self.webSocketAddress))

    def on_open(self, ws):
        self.BMCCConnectionState = BMCCConnectionState.CONNECTED
        self.inputQueue.put(BMCCMessage(self.get_camname(), BMCCMessageType.CAMSTATE, self.BMCCConnectionState.name))
        logging.info("ws: {} :CONNECTED {}".format(self.get_camname(),self.webSocketAddress))

        # clear the queues
        with self.outputQueue.mutex:
            self.outputQueue.queue.clear()

        # configure the connection
        try:
            time.sleep(.1)
            # send init message
            json_out = get_subscribe_all_message()
            logging.debug("ws: {} :SND_MSG {}".format(self.get_camname(),json_out))
            ws.send(json_out)
            time.sleep(.1)
            # unsubscribe timecode
            json_out = get_unsubscribe_channel_message()
            logging.debug("ws: {}  :SND_MSG {}".format(self.get_camname(),json_out))
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
                logging.debug("ws: {} :SND_MSG {}".format(self.get_camname(),json_out))
                try:
                    ws.send(json_out)
                except WebSocketConnectionClosedException:
                    logging.debug("ws: {} WebSocketConnectionClosedException".format(self.get_camname()))
                    self.close_connection()
                    return
                time.sleep(.01)

        _thread.start_new_thread(run, ())

    def __init__(self, dataQueueIn: Queue, dataQueueOut: Queue, camera , enableTrace=False,
                 autoRecover=True, pingInterval=15, pingTimeout=1):
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
            self.BMCCConnectionState = BMCCConnectionState.CONNECTING
            self.inputQueue.put(
                BMCCMessage(self.get_camname(), BMCCMessageType.CAMSTATE, self.BMCCConnectionState.name))
            logging.debug("ws: {} :CONNECT ".format(self.get_camname()))
            self.ws = websocket.WebSocketApp(self.webSocketAddress,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close)
            self.ws.run_forever(ping_interval=15, ping_timeout=1)
            self.BMCCConnectionState = BMCCConnectionState.DISCONNECTED
            self.inputQueue.put(
                BMCCMessage(self.get_camname(), BMCCMessageType.CAMSTATE, self.BMCCConnectionState.name))

            if self.autoRecover:
                time.sleep(5)
                while not self.outputQueue.empty():
                    if self.outputQueue.get() is None:
                        self.autoRecover = False
                if self.autoRecover:
                    logging.debug("ws: {} :RECONNECT".format(self.get_camname()))

class AsyncMessageProcessor:

    camera = None
    command_queue: Queue = None
    atem = None
    command_queue_thread_running = False

    def get_camname(self):
        return self.camera.name if self.camera else "None"

    def __init__(self, camera=None, command_queue=None, ws_queue=None, atem=None):
        self.camera=camera
        self.command_queue=command_queue
        self.atem=atem
        self.ws_queue=ws_queue

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
            try:
                self.camera.async_state = BMCCConnectionState[message.message]
                logging.debug(
                "process_async_message CAMSTATE: CAM " + message.src + " State changed to: " + str(message.message))
            except KeyError:
                logging.error(
                    f"process_async_message GOT INVALID STATE {message.message}")
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

    def start_command_queue_processing(self):
        if self.command_queue==None:
            logging.warning("No command_queue is defined (is None). Not starting thread.")
            return

        if self.command_queue_thread_running:
            logging.error("Command Queue already running. Not starting thread.")
            return

        def run(*args):
            self.command_queue_thread_running = True
            while True:
                command = self.command_queue.get()
                if command is None:
                    if self.atem:
                        self.atem.atem_disconnect()
                        self.atem.state = BMCCAtemState.CLOSED
                    self.command_queue_thread_running = False
                    return
                if type(command) is BMCCMessage:
                    if command.command:
                        if type(command.command) is BMCCMessageCommands:
                            if command.type == BMCCMessageType.ATEM:
                                self.process_atem_command(command)
                            elif command.type == BMCCMessageType.REST:
                                self.process_rest_command(command)
                            elif command.type == BMCCMessageType.JSON:
                                self.process_json_command(command)
                            time.sleep(command.delay)
                        else:
                            logging.warning(f"async: {command.command} is not a BMCCMessageCommand")
                    else:
                        logging.warning(f"async: command is None")
                else:
                    logging.warning(f"async: command is not a BMCCMessage, is a {type(command)}")
                time.sleep(.01)

        _thread.start_new_thread(run, ())

    def process_json_command(self, command: BMCCMessage):
        if self.ws_queue:
            self.ws_queue.put(command.message)
        else:
            logging.warning("async: can't send JSON message because ws_queue is None")

    def process_rest_command(self, command:BMCCMessage):
        from PyBMCC.Camera import REST_MODULE_MAP
        from PyBMCC.Enums import CameraState

        if self.camera is None:
            logging.warning("async: can't send REST message because camera is None")
            return
        if self.camera.state != CameraState.CONNECTED:
            logging.warning("async: camera is not in a connected state")
        logging.debug(f"async rest {self.camera.host_or_ipaddr}: {self.get_camname()} :EXE_MSG {command.command.name} {command.args}")

        #build the function name
        cmd_split=(command.command.name).split("_")
        cat = cmd_split[2]
        cmd = "_".join(cmd_split [3:])
        if cmd_split[0]!="do":
            cmd="_".join([cmd_split[0],cmd])

        if cat not in REST_MODULE_MAP:
            logging.error(f"async rest {self.camera.host_or_ipaddr}: {command.command.name} is not an implemented REST command. Category {cat} unknown.")
            return

        if not command.args:
            command.args = {}

        #if timestamp field, we are cloning. Remove ts and convert keys to snake case
        if 'ts' in command.args:
            newargs = {}
            for key, value in command.args.items():
                sc=CC2SC.sub('_', key).lower()
                newargs[sc]=value
            del newargs['ts']
            command.args=newargs

        try:
            fn = getattr(REST_MODULE_MAP[cat], cmd, None)
            obj= getattr(self.camera, cat, None)
        except AttributeError:
            logging.error(
                f"async rest {self.camera.host_or_ipaddr}: {command.command.name} not found. FIXME.")
            return

        if fn is not None and obj is not None:
            if cmd_split[0] == "get":
                self.camera.last_command = cmd
                self.camera.last_command_ts = time.time()
            result=fn(obj, **command.args)
            if cmd_split[0] == "get":
                logging.debug(
                    f"async rest {self.camera.host_or_ipaddr}: LAST RESULT: {result}")
                self.camera.last_command_result = result
                self.camera.last_command_result_ts = time.time()
            if command.callback:
                if callable(command.callback):
                    command.callback(**{'result':result,'command':command,'camera':self.camera})

        else:
            logging.warning(f"async rest {self.camera.host_or_ipaddr}: {command.command.name} is not an implemented REST command")

    def process_atem_command(self,command:BMCCMessage):
        if self.atem is None:
            logging.warning("async atem: can't send REST message because atem is None")
            return
        if self.atem.state != BMCCConnectionState.CONNECTED:
            logging.warning("async atem: atem is not in a connected state")
        logging.debug(f"async atem {self.atem.atem_ipaddr}: {self.get_camname()} :EXE_MSG {command.command.name} {command.args}")

        if not command.args:
            command.args = {}

        #reassign the camera if required
        if "destination_device" not in command.args and self.camera is not None:
            if self.camera.atem_id != 0:
                logging.warning(f"async atem {self.atem.atem_ipaddr}: retargeting message to camera ATEM ID"
                    +f"None->{self.camera.atem_id}.")
                command.args['destination_device']=self.camera.atem_id
        elif "destination_device" in command.args and self.camera is not None:
            if self.camera.atem_id not in [0,ALL_CAMERAS] and command.args["destination_device"] != self.camera.atem_id:
                logging.warning(f"async atem {self.atem.atem_ipaddr}: retargeting message to camera ATEM ID"
                        +f"{command.args['destination_device']}->{self.camera.atem_id}.")
                command.args["destination_device"]=self.camera.atem_id

        fn = getattr(ATEM, command.command.name, None)
        if fn is not None:
            fn(self.atem , **command.args)
            if command.callback:
                if callable(command.callback):
                    command.callback(**{'result':None,'command':command,'camera':self.camera})
        else:
            logging.warning(f"async atem {self.atem.atem_ipaddr}: {command.command.name} is not an implemented ATEM command")

def get_subscribe_all_message() -> str:
    return '{"data": {"action": "subscribe", "properties": ["*"]}, "type": "request"}'
def get_unsubscribe_channel_message(channel="/transports/0/timecode") -> str:
    return '{"data": {"action": "unsubscribe", "properties": ["'+str(channel)+'"]}, "type": "request"}'
