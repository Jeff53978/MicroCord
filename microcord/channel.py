from types import SimpleNamespace

from .user import User

class Channel:
    def __init__(self, token: str, data: object):
        self.token = token
        self.type = data.type
        self.position = data.position
        self.permission_overwrites = data.permission_overwrites
        self.name = data.name
        self.id = data.id
        self.last_message_id = data.last_message_id

    def __repr__(self):
        return f"MicroCord.Channel(type={self.type}, position={self.position}, permission_overwrites={self.permission_overwrites}, name={self.name}, id={self.id}, last_message_id={self.last_message_id})"