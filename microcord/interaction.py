import requests

from types import SimpleNamespace
from .user import User

class Interaction:
    def __init__(self, data: object):
        self.id = data.id
        self.token = data.token
        self.name = data.data["name"]
        self.author = User(self.token, SimpleNamespace(**data.member["user"]))

    def reply(self, content: str = None, embed: object = None):
        payload = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": [embed.to_dict()] if embed else []
            }
        }
        requests.post(f"https://discord.com/api/interactions/{self.id}/{self.token}/callback", json=payload)