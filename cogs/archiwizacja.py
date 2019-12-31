import discord
from discord.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.logsChannel = self.bot.get_channel(660770250001874944)
        self.errorChannel = self.bot.get_channel(660813978154303518)

    async def send_log(self, send_channel: discord.TextChannel, msg: discord.Message, desc: str,
                       msg_color: discord.Color):
        """WYSYŁANIE WIADOMOSCI DO LOGOW, DO WSKAZANEGO KANAŁU"""
        if msg.channel != self.logsChannel and msg.author.id != self.bot.user.id:
            msg_em = discord.Embed(
                title=msg.author,
                description=desc,
                colour=msg_color
            )

            msg_em.set_footer(
                text=f'{msg.channel}, ID: {msg.author.id}'
            )

            await send_channel.send(embed=msg_em)

    @commands.Cog.listener()
    async def on_message(self, message):
        self.send_log(self.logsChannel, message, f"Wiadomość: {message.content}", discord.Color.green())

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.send_log(self.logsChannel, message, f"Wiadomość: {message.content}", discord.Color.green())

    @commands.Cog.listener()
    async def on_error(self, message):
        await self.send_log(self.errorChannel, message, message.content, discord.Color.dark_red())


def setup(bot):
    bot.add_cog(Logs(bot))
