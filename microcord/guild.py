from types import SimpleNamespace

from .user import User
from .channel import Channel

class Guild:
    def __init__(self, token: str, data: object):
        self.token = token
        self.emojis = data.emojis
        self.joined_at = data.joined_at
        self.premium_subscription_count = data.premium_subscription_count
        self.members = [User(self.token, i.user) for i in data.members]
        self.icon = data.icon
        self.preffered_locale = data.preffered_locale
        self.roles = None
        self.channels = [Channel(self.token, i) for i in data.channels]
        self.member_count = data.member_count
        self.name = data.name

    def __repr__(self):
        return f"MicroCord.Guild(emojis={self.emojis}, joined_at={self.joined_at}, premium_subscription_count={self.premium_subscription_count}, members={self.members}, icon={self.icon}, preferred_locale={self.preffered_locale}, roles={self.roles}, channels={self.channels}, member_count={self.member_count}, name={self.name})"