import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids


class Info(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="info", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="user",
            description="Wyświetlenie danych użytkownika",
            option_type=SlashCommandOptionType.USER,
            required=False
        )
    ])
    async def __info(self, ctx: SlashContext, user: discord.Member = None):
        await ctx.ack(True)

        user = user or ctx.author
        informacje = {
            "Nick": user.name,
            "ID": user.id,
            "Status": user.status,
            "Najwyższa rola": user.top_role,
            "Dołączył/a": user.joined_at,
            "#": user.discriminator,
            "Avatar": user.avatar_url,
            "Server": user.guild
        }
        wiadomosc = ""
        for key, value in informacje.items():
            wiadomosc += key + " : " + str(value) + "\n"
        em = discord.Embed(
            title=f"Informacje o {informacje['Nick']}", description=wiadomosc, colour=discord.Colour.green())
        await ctx.send(embed=em)


def setup(bot: TeinfBot):
    bot.add_cog(Info(bot))
