import websocket
import threading
import requests
import json
import time

from types import SimpleNamespace
from functools import wraps

from .user import User
from .message import Message
from .interaction import Interaction

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
        self.commands = []
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bot {self.token}"
        })
        x = self.session.get("https://discord.com/api/users/@me")
        if x.status_code == 401:
           print("[ Error ] Token invalid")
           exit()
        else:
            self.id = x.json()["id"]
        self.ready = None
        self.guild_create = None
        self.message_create = None

    def command(self, name: str = None, description: str = None, json: dict = None, guild_id: int = None):
        def decorator(function):
            if name and description:
                payload = {
                    "name": name,
                    "type": 1,
                    "description": description,
                }
            if json:
                payload = json
            if guild_id:
                self.session.post(f"https://discord.com/api/applications/{self.id}/guilds/{guild_id}/commands", json=payload)
            else:
                self.session.post(f"https://discord.com/api/applications/{self.id}/commands", json=payload)
            self.commands.append({"name": name, "function": function})
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)
            return wrapper
        return decorator

    def event(self, event: str = None):
        def decorator(function):
            if event == "READY": self.ready = function
            if event == "GUILD_CREATE": self.guild_create = function
            if event == "MESSAGE_CREATE": self.message_create = function
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)
            return wrapper
        return decorator

    def event_handler(self):
        while True:
            try:
                msg = GatewayMessage(self.ws.recv())
                if msg.op == 11:
                    pass
                else: 
                    if msg.event == "READY" and self.ready:
                        self.user = User(self.token, SimpleNamespace(**msg.data.user))
                        threading.Thread(target=self.ready).start()

                    if msg.event == "MESSAGE_CREATE" and self.message_create:
                        threading.Thread(target=self.message_create, args=(Message(self.token, msg.data),)).start()

                    if msg.event == "INTERACTION_CREATE":
                        for command in self.commands:
                            if command["name"] == msg.data.data["name"]:
                                threading.Thread(target=command["function"], args=(Interaction(msg.data),)).start()

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
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "microcord",
                    "$device": "microcord"
                },
            }
        }))

    def run(self, intents: int = 3243773):
        self.intents = intents
        self.ws = websocket.create_connection("wss://gateway.discord.gg/?v=6&encoding=json")
        self.interval = GatewayMessage(self.ws.recv()).data.heartbeat_interval / 1000
        threading.Thread(target=self.authentication_handler).start()
        threading.Thread(target=self.connection_handler).start()
        threading.Thread(target=self.event_handler).start()
