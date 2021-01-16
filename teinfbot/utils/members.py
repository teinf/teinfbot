import discord
from typing import List
from teinfbot import TeinfBot

class MembersUtils:

    AFK_CHANNEL_ID = 423934688244006913

    @staticmethod
    def get_online_members(bot: TeinfBot) -> List[discord.Member]:
        members: List[discord.Member] = []
        for channel in bot.get_all_channels():
            if str(channel.type) == "voice" and channel.id != MembersUtils.AFK_CHANNEL_ID:
                for member in channel.members:
                    members.append(member)
        return members