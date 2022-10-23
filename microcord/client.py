from code import interact
import websocket
import asyncio
import json

from types import SimpleNamespace

class GatewayMessage():
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
        self.loop = asyncio.get_event_loop()
        self.token = token

    def event(self, event: str = None):
        self.loop.create_task(self.event_handler(event))

    async def event_handler(self, event: str = None):
        while True:
            msg = GatewayMessage(self.ws.recv())
            if msg.op == 11:
                print("Heartbeat acknowledged!")
            else: 
                print(msg.event)
            await asyncio.sleep(0.1)

    async def connection_handler(self):
        print("Starting connection handler...")
        while self.interval:
            self.ws.send(json.dumps({
                "op": 1,
                "d": None
            }))
            print("Heartbeat sent!")
            await asyncio.sleep(self.interval)
        else:
            print("Heartbeat interval is 0, stopping heartbeat.")

    def authentication_handler(self):
        print("Authenticating with Discord...")
        self.ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "linux",
                    "$browser": "microcord",
                    "$device": "microcord"
                },
            }
        }))
        print("Authenticated with Discord!")

    def run(self):
        self.ws = websocket.create_connection("wss://gateway.discord.gg/?v=6&encoding=json")
        self.interval = GatewayMessage(self.ws.recv()).data.heartbeat_interval / 1000
        self.authentication_handler()
        self.loop.run_until_complete(self.connection_handler())