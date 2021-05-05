import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.db import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.guilds import guild_ids
from teinfbot.utils.levels import LevelsUtils


class Level(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="level", description="Wyświetla poziom", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="user",
            description="Użytkownik",
            option_type=SlashCommandOptionType.USER,
            required=False
        )
    ])
    async def __level(self, ctx: SlashContext, user: discord.Member = None):
        
        user = user or ctx.author
        teinf_user: TeinfMember = db_session.query(TeinfMember).filter_by(discordId=user.id).first()
        level = LevelsUtils.levelFromExp(teinf_user.exp)
        next_level_exp = LevelsUtils.expFromLevel(level + 1)
        missing_exp_to_lvlup = int(next_level_exp - teinf_user.exp)

        embed = discord.Embed(
            title="💎 LEVEL 💎",
            description=f"Wykres poziomu {user.mention}\n`{level}LVL - {teinf_user.exp}EXP.`\nBrakuje `{missing_exp_to_lvlup}` do kolejnego poziomu.",
            color=discord.Color.blue()
        )

        embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


def setup(bot: TeinfBot):
    bot.add_cog(Level(bot))
