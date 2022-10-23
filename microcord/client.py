import websocket
import threading
import json
import time

from types import SimpleNamespace
from functools import wraps

from .user import User

class GatewayMessage:
    def __init__(self, data: str):
        try:
            data = json.loads(data)
            self.op = data["op"]
            if data["d"]:
                self.data = SimpleNamespace(**data["d"])
            else:
                self.data = None
            if "t" in data:
                self.event = data["t"]
            else:
                self.event = None
        except:
            self.op = None
            self.data = None
            self.event = None

class Client:
    def __init__(self, token):
        self.token = token

        self.ready = None
        self.guild_create = None
        self.message_create = None

    def event(self, event: str = None):
        def decorator(function):
            if event == "READY": self.ready = function
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)
            return wrapper
        return decorator

    def event_handler(self, event: str = None):
        while True:
            try:
                msg = GatewayMessage(self.ws.recv())
                if msg.op == 11:
                    pass
                else: 
                    if msg.event == "READY" and self.ready:
                        self.user = User(self.token, SimpleNamespace(**msg.data.user))
                        self.ready()
            except websocket._exceptions.WebSocketConnectionClosedException:
                print("Socket closed")
                exit()

    def connection_handler(self):
        while self.interval:
            self.ws.send(json.dumps({
                "op": 1,
                "d": None
            }))
            time.sleep(self.interval)

    def authentication_handler(self):
        self.ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "intents": 3243773,
                "properties": {
                    "$os": "linux",
                    "$browser": "microcord",
                    "$device": "microcord"
                },
            }
        }))

    def run(self):
        self.ws = websocket.create_connection("wss://gateway.discord.gg/?v=6&encoding=json")
        self.interval = GatewayMessage(self.ws.recv()).data.heartbeat_interval / 1000
        threading.Thread(target=self.authentication_handler).start()
        threading.Thread(target=self.connection_handler).start()
        threading.Thread(target=self.event_handler).start()