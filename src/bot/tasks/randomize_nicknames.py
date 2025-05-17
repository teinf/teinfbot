from discord.ext import tasks, commands

from bot import Bot
from random_nickname import get_random_name
from config import config

import logging

logger = logging.getLogger(__name__)


class NicknameRandomizer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.randomize_nicknames.start()

    def cog_unload(self):
        self.randomize_nicknames.cancel()

    @tasks.loop(hours=24)
    async def randomize_nicknames(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(self.bot.guild.id)
        if not guild:
            return

        users_to_change = [
            config.dc.random_nickname_user_id
        ]  # Replace with real user IDs
        channel = guild.get_channel(
            config.dc.random_nickname_channel_id
        )  # Logging channel

        for user_id in users_to_change:
            member = guild.get_member(user_id)
            if not member:
                continue

            new_nick = get_random_name()

            try:
                await member.edit(nick=new_nick)
                if channel:
                    await channel.send(
                        f"✅ Zmieniono nick {member.mention}: `{new_nick}`"
                    )
            except Exception as e:
                print(f"Failed: {e}")

    @randomize_nicknames.before_loop
    async def before_randomize_nicknames(self):
        await self.bot.wait_until_ready()


async def setup(bot: Bot):
    await bot.add_cog(NicknameRandomizer(bot))
