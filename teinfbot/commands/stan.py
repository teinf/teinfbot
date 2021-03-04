import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.db import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.guilds import guild_ids


class Stan(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="stan", guild_ids=guild_ids, description="Wyświetla stan konta", options=[
        manage_commands.create_option(
            name="user",
            description="Użtykownik",
            option_type=SlashCommandOptionType.USER,
            required=False
        )
    ])
    async def __stan(self, ctx: SlashContext, user: discord.Member):
        await ctx.ack(False)
        if user is None:
            user = ctx.author

        teinf_member: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=user.id).first()

        embd = discord.Embed(
            title="💵  TEINF BANK  💵",
            description=f"Stan konta {user.mention}:\n`- {teinf_member.money} chillcoinów`",
            color=discord.Color.green()
        )

        await ctx.send(embed=embd)


def setup(bot: TeinfBot):
    bot.add_cog(Stan(bot))
