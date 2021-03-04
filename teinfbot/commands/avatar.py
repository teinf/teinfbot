import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids


class Avatar(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="avatar", description="Wyświetla avatar gracza", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="user",
            description="Użytkownik",
            option_type=SlashCommandOptionType.USER,
            required=False
        )
    ])
    async def __avatar(self, ctx: SlashContext, user: discord.Member = None):
        await ctx.ack(True)
        user = user or ctx.author
        await ctx.send(f"{user.avatar_url}")


def setup(bot: TeinfBot):
    bot.add_cog(Avatar(bot))
