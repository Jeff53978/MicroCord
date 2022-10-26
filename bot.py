import microcord

from microcord.events import ready, message_create

client = microcord.Client("asdasdasd")

@client.event(ready)
def on_ready():
    print(f"[ INFO ] Logged in as {client.user.username}#{client.user.discriminator}")

@client.event(message_create)
def on_message(msg):
    print(f"[ {msg.author.username} ] {msg.content}")

@client.command(name="ping", description="Pings the bot", guild_id=int(open(".guild_id", "r").read()))
def ping_command(msg):
    print(f"[ {msg.author.username} ] /ping")
    embed = microcord.Embed("Pong!", "This bot is running", 0xfafafa)
    msg.reply(embed=embed)

client.run(microcord.Intents.all())
