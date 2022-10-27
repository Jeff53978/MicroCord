import websocket
import threading
import requests
import json
import time

from munch import DefaultMunch
from functools import wraps

from .user import User
from .message import Message
from .interaction import Interaction
from .guild import Guild

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
        self.ready = False
        self.guild_create = None
        self.message_create = None
        self.guild_create = None
        self.session_id = None
        self.resume_gateway_url = None
        self.user = None
        self.guilds = None

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
                data = json.loads(self.ws.recv())
                i = DefaultMunch.fromDict(data)
                if i.op == 11:
                    pass

                elif i.t == "READY" and self.ready:
                    self.session_id = i.d.session_id
                    self.resume_gateway_url = i.d.resume_gateway_url
                    self.user = User(self.token, i.d.user)
                    self.guilds = [Guild(self.token, x) for x in DefaultMunch.fromDict(self.session.get("https://discord.com/api/users/@me/guilds").json())]
                    self.ready()

                elif i.t == "MESSAGE_CREATE" and self.message_create:
                    self.message_create(Message(self.token, i.d))

                else:
                    print(i.t)
                    
            except Exception as e:
                print(e)
                print("[ Error ] Socket closed")
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
        self.interval = json.loads(self.ws.recv())["d"]["heartbeat_interval"] / 1000
        threading.Thread(target=self.authentication_handler).start()
        threading.Thread(target=self.connection_handler).start()
        threading.Thread(target=self.event_handler).start()
