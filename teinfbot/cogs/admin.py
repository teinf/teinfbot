from discord.ext import commands

from teinfbot import TeinfBot
from teinfbot import db_session
from teinfbot.models import TeinfMember


class Admin(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    def refill_members(self, add_confirmation: bool = False):
        for member in self.bot.get_all_members():
            STARTING_MONEY = 300
            tm = TeinfMember(int(member.id), STARTING_MONEY, 0)
            db_session.add(tm)
            if add_confirmation:
                print(f"Dodano {member.name}")


def setup(bot):
    bot.add_cog(Admin(bot))
