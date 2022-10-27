from types import SimpleNamespace
from munch import DefaultMunch

import requests

from .user import User
from .channel import Channel

class Guild:
    def __init__(self, token: str, data: object):
        self.token = token
        self.id = data.id
        self.emojis = data.emojis if data.emojis else None
        self.joined_at = data.joined_at if data.joined_at else None
        self.premium_subscription_count = data.premium_subscription_count
        self.icon = data.icon
        self.preffered_locale = data.preffered_locale
        self.roles = None
        self.member_count = data.member_count
        self.name = data.name

    def __repr__(self):
        return f"MicroCord.Guild(emojis={self.emojis}, joined_at={self.joined_at}, premium_subscription_count={self.premium_subscription_count}, icon={self.icon}, preferred_locale={self.preffered_locale}, roles={self.roles}, member_count={self.member_count}, name={self.name}, id={self.id})"