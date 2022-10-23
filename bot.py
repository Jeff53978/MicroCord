import microcord

client = microcord.Client(open(".token", "r").read())

@client.event
async def ready():
    print("Ready!")

client.run()