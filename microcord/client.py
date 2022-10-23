from code import interact
import websocket
import asyncio
import json

from types import SimpleNamespace

class GatewayMessage():
    def __init__(self, data: str):
        data = json.loads(data)
        self.op = data["op"]
        self.data = SimpleNamespace(**data["d"])
        if "name" in data:
            self.name = data["name"]
        else:
            self.name = None

class Client:
    def __init__(self, token):
        self.token = token
        self.ws = websocket.create_connection("wss://gateway.discord.gg/?v=6&encoding=json")
        self.interval = GatewayMessage(self.ws.recv()).data.heartbeat_interval / 1000
        loop = asyncio.get_event_loop()
        loop.create_task(self.authentication_handler())

    def event(self, event: str = None):
        loop = asyncio.get_event_loop()
        loop.create_task(self.event_handler(event))

    async def event_handler(self, event: str):
        while True:
            data = GatewayMessage(self.ws.recv())
            print(data)

    async def connection_handler(self):
        while self.interval:
            self.ws.send(json.dumps({
                "op": 1,
                "d": None
            }))
            print("Heartbeat sent!")
            await asyncio.sleep(self.interval)

    async def authentication_handler(self):
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
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connection_handler())