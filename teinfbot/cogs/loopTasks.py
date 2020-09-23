from discord.ext import commands, tasks
import discord
import random
from teinfbot import TeinfBot
from teinfbot.paths import PATH_ASSETS
import os

class LoopTasks(commands.Cog):

    def __init__(self, bot: TeinfBot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.arrow.start()
    
    @tasks.loop(hours=24)
    async def arrow(self):
        teinf = self.bot.get_guild(self.bot.guild_id)

        ARROW_ID = 239329824361938944
        user = teinf.get_member(ARROW_ID)
        if not user:
            return
        
        randomPrzymiotnik = self.randomRowFromFile(os.path.join(PATH_ASSETS, 'przymiotniki.txt'))
        randomRzeczownik  = self.randomRowFromFile(os.path.join(PATH_ASSETS, 'rzeczowniki.txt'))
        randomNickname = randomPrzymiotnik + " " + randomRzeczownik
            
        await user.edit(nick=randomNickname)

        channel = teinf.get_channel(720628646267584572)
        await channel.send(f"ARROW: {randomNickname}")
    
    @staticmethod
    def randomRowFromFile(file):
        with open(file, "r") as f:
            if not f.closed:
                return random.choice(f.readlines()).strip()


def setup(bot):
    bot.add_cog(LoopTasks(bot))
