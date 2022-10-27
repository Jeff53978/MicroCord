class User:
    def __init__(self, token: str, data: object):
        self.token = token
        self.username = data.username
        self.id = data.id
        self.discriminator = data.discriminator
        self.avatar = data.avatar

        try: self.verified = data.verified
        except: self.verified = None
        try: self.bot = data.bot
        except: self.bot = None

    def __repr__(self):
        return f"MicroCord.User(username={self.username}, id={self.id}, discriminator={self.discriminator}, avatar={self.avatar}, verified={self.verified}, bot={self.bot})"