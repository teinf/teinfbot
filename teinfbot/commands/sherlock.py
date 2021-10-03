import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids

from teinfbot.lib.sherlock import sherlock


class Sherlock(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="sherlock", description="Wyświetla konta użytkownika na stronach", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="user",
            description="Nazwa użytkownika",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ])
    async def __sherlock(self, ctx: SlashContext, user: str):

        await ctx.defer()
        result = sherlock.get_user(user)

        desc = ""
        for r in result:
            desc += f"[🔹] **{r.site_name}:** {r.site_url_user}\n"
        em = discord.Embed(title="🕵️‍♂️ Sherlock",
                           description=desc)
        await ctx.send(embed=em)


def setup(bot: TeinfBot):
    bot.add_cog(Sherlock(bot))
