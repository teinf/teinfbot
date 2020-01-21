import discord
import os

client = discord.Client()


@client.event
async def on_ready():
    chan = client.get_channel(668140025061441570)
    usr: discord.User = client.get_user(354322592787857408)

    embd = discord.Embed(
        title="Kamil",
        description=f"{usr.mention}."
    )

    await chan.send(embed=embd)


client.run(os.environ["ACCESS_TOKEN"])
