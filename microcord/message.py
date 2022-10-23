from types import SimpleNamespace

from .user import User

class Message:
    def __init__(self, token: str, data: object):
        self.token = token
        self.timestamp = data.timestamp
        self.pinned = data.pinned
        self.mentions = data.mentions
        self.id = data.id
        self.author = User(self.token, SimpleNamespace(**data.author))
        self.attachments = data.attachments
        self.content = data.content