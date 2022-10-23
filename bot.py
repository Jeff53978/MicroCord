import microcord

client = microcord.Client(open(".token", "r").read())

@client.event("ready")
async def ready():
    pass