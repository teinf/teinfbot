import asyncio
import discord
from discord.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.logChannelID = 660770250001874944
        self.logsChannel = bot.get_channel(self.logChannelID)

    @commands.Cog.listener()
    async def on_message(self, message):
        # wysyłanie wiadomosci do logów
        if message.channel.id != logChannelID and message.author.id != bot.user.id:
            msgEm = discord.Embed(
                title=f"{message.author}", description=f"Wiadomość: {message.content}", colour=discord.Color.green())
            msgEm.set_footer(
                text=f'{message.channel}, ID: {message.author.id}')
            logsChannel = bot.get_channel(logChannelID)
            await logsChannel.send(embed=msgEm)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # wysyłanie wiadomosci do logów
        if message.channel.id != logChannelID and message.author.id != bot.user.id:
            msgEm = discord.Embed(
                title=f"USUNIĘTO: {message.author}", description=f"Wiadomość: {message.content}", colour=discord.Color.red())
            msgEm.set_footer(
                text=f'{message.channel}, ID: {message.author.id}')
            logsChannel = bot.get_channel(logChannelID)
            await logsChannel.send(embed=msgEm)


def setup(bot):
    bot.add_cog(Logs(bot))
