import discord
from typing import List

class ChannelUtils:
    @staticmethod
    def is_private_channel(channel: discord.TextChannel):
        return str(channel.type) == "private"
