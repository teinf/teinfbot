import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from teinfbot.bot import TeinfBot
from teinfbot.db import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.guilds import guild_ids
from teinfbot.utils.time import TimeUtils

from typing import List


class Top(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="top", guild_ids=guild_ids)
    async def __top(self, ctx: SlashContext):
        await ctx.ack(True)

        topTimeSpentMembers: List[TeinfMember] = db_session.query(TeinfMember).order_by(TeinfMember.timespent).all()
        i = 1

        topkaTitle = "TOP CZASU"
        topkaDescription = ""

        for member in topTimeSpentMembers[::-1]:
            if i > 10:
                break

            mention = f"<@{member.discordId}>"

            topkaDescription += f"{i}. {mention:15} {TimeUtils.getTimeDescFromMinutes(member.timespent)}\n"
            i += 1

        em = discord.Embed(
            title=topkaTitle,
            description=topkaDescription,
            color=discord.Color.gold()
        )

        await ctx.send(embed=em)


def setup(bot: TeinfBot):
    bot.add_cog(Top(bot))
