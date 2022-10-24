# MicroCord
Microcord is an minimal Discord library with slash commands, made for simple bots

# Example

```py
import microcord

from microcord.events import ready, message_create

client = microcord.Client("YOUR TOKEN HERE")

@client.event(ready)
def on_ready():
    print(f"[ INFO ] Logged in as {client.user.username}#{client.user.discriminator}")

@client.event(message_create)
def on_message(msg):
    print(f"[ {msg.author.username} ] {msg.content}")

@client.command(name="ping", description="Pings the bot", guild_id=int(GUILD ID HERE))
def ping_command(msg):
    print(f"[ {msg.author.username} ] /ping")
    embed = microcord.Embed("Pong!", "This bot is running", 0xfafafa)
    msg.reply(embed=embed)

client.run(intents=3243773)
```
