import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids
from teinfbot.utils.api.random_user import RandomUserApi, User

class RandomUser(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="randomuser", description="Wyświetla losową osobę", guild_ids=guild_ids)
    async def __randomuser(self, ctx: SlashContext):
        await ctx.ack(True)
        random_user: User = await RandomUserApi.get_random_user_async()

        em = discord.Embed()
        em.set_author(name=random_user.name.first + " " + random_user.name.last, icon_url=random_user.picture.thumbnail)
        em.add_field(name="Telefon", value=random_user.phone)
        em.add_field(name="Wiek", value=random_user.dob.age)
        em.add_field(name="Data urodzenia", value=random_user.dob.date)
        em.add_field(name="Email", value=random_user.email)
        em.add_field(name="Płeć", value=random_user.gender)
        em.add_field(name="Login", value=random_user.login.username)
        em.add_field(name="Hasło", value=random_user.login.password)
        em.add_field(name="Kraj", value=random_user.location.country)
        em.add_field(name="Miasto", value=random_user.location.city)
        em.add_field(name="Tytuł", value=random_user.name.title)
        em.add_field(name="Pochodzenie", value=random_user.nat)
        em.add_field(name="Data rejestracji", value=random_user.registered.date)
        em.add_field(name="Telefon", value=random_user.cell)

        em.set_image(url=random_user.picture.large)

        await ctx.send(embed=em)


def setup(bot: TeinfBot):
    bot.add_cog(RandomUser(bot))
