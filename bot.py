import microcord

client = microcord.Client(open(".token", "r").read())

@client.event("READY")
def test_function():
    print(f"[ INFO ] Logged in as {client.user.username}#{client.user.discriminator}")

@client.event("MESSAGE_CREATE")
def test_function2(msg):
    print(f"[ {msg.author.username} ] {msg.content}")

client.run()