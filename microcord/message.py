from types import SimpleNamespace

from .user import User

class Message:
    def __init__(self, token: str, data: object):
        self.token = token
        self.timestamp = data.timestamp
        self.pinned = data.pinned
        self.mentions = data.mentions
        self.id = data.id
        self.author = User(self.token, data.author)
        self.attachments = data.attachments if data.attachments else None
        self.content = data.content if data.content else None

    def __repr__(self):
        return f"MicroCord.Message(timestamp={self.timestamp}, pinned={self.pinned}, mentions={self.mentions}, id={self.id}, author={self.author}, attachments={self.attachments}, content={self.content})"