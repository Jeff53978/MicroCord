import microcord

client = microcord.Client(open(".token", "r").read())

@client.event("READY")
def test_function():
    print(f"[ INFO ] Logged in as {client.user.username}#{client.user.discriminator}")

@client.event("MESSAGE_CREATE")
def test_function2(msg):
    print(f"[ {msg.author.username} ] {msg.content}")

@client.command(name="ping", description="Pings the bot", guild_id=int(open(".guild_id", "r").read()))
def ping_command(msg):
    print(f"[ {msg.author.username} ] /ping")
    msg.reply("Pong!")

client.run(intents=3243773)