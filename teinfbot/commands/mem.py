import random

from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids
from teinfbot.utils.memes import JbzdMeme, KwejkMeme


class Mem(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="mem", description="Wysyła losowego mema!", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="strona",
            description="Strona z której mają zostać wybrane memy",
            option_type=SlashCommandOptionType.STRING,
            required=False,
            choices=['jbzd.pl', 'kwejk.pl']
        ),
    ])
    async def __mem(self, ctx: SlashContext, strona: str = None):
        await ctx.ack(True)

        strona = strona or random.choice(['jbzd.pl', 'kwejk.pl'])
        if strona == 'jbzd.pl':
            random_meme = await JbzdMeme.random_meme_async()
            await ctx.send(embed=random_meme.embed)
        elif strona == 'kwejk.pl':
            random_meme = await KwejkMeme.random_meme_async()
            await ctx.send(embed=random_meme.embed)


def setup(bot: TeinfBot):
    bot.add_cog(Mem(bot))
