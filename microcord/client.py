import websocket
import threading
import json
import time

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
        self.token = token
        self.connected = False

    def event(self, event: str = None):
        threading.Thread(target=self.event_handler, args=(event,)).start()

    def event_handler(self, event: str = None):
        while self.connected:
            try:
                msg = GatewayMessage(self.ws.recv())
                if msg.op == 11:
                    print("Heartbeat acknowledged!")
                else: 
                    print(msg.event)
            except websocket._exceptions.WebSocketConnectionClosedException:
                print("Socket closed")

    def connection_handler(self):
        print("Starting connection handler...")
        while self.interval:
            self.ws.send(json.dumps({
                "op": 1,
                "d": None
            }))
            print("Heartbeat sent!")
            time.sleep(self.interval)
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
        self.connected = True
        threading.Thread(target=self.connection_handler).start()
        threading.Thread(target=self.authentication_handler).start()