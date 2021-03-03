import discord


class ChannelUtils:
    @staticmethod
    def is_private_channel(channel: discord.TextChannel):
        return str(channel.type) == "private"
