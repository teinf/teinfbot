import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.db import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.guilds import guild_ids
from teinfbot.utils.time import TimeUtils


class Czas(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="czas", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="user",
            description="Wyświetlenie czasu użytkownika na serwerze",
            option_type=SlashCommandOptionType.USER,
            required=False
        )
    ])
    async def __czas(self, ctx: SlashContext, user: discord.Member = None):
        await ctx.ack(True)

        user = user or ctx.author

        teinfMember: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=user.id).first()

        em = discord.Embed(
            title="Czas spędzony na serwerze",
            description=f"{user.display_name} spędził {TimeUtils.getTimeDescFromMinutes(teinfMember.timespent)} na serwerze",
            color=discord.Colour.green()
        )
        await ctx.send(embed=em)


def setup(bot: TeinfBot):
    bot.add_cog(Czas(bot))
