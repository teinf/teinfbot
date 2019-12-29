import asyncio
import random
import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup

totalTemplate = "Total: {}"
onlineTemplate = "Online: {}"
offlineTemplate = "Offline: {}"

if __name__ == "__main__":
  print("Refreshed stats...")
  r = requests.get('https://teamtrees.org')
  r = r.text
  soup = BeautifulSoup(r, "html.parser")

  match = soup.find('div', class_="counter")
  treesAmount = int(match["data-count"])
  print("{0:,}".format(treesAmount))

class ServerStats(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      # channels
      # self.onlineChannel = self.bot.get_channel(599189850859503621)
      # self.offlineChannel = self.bot.get_channel(599195472590143556)
      # self.totalChannel = self.bot.get_channel(599189928584282142)
      self.treeChannel = self.bot.get_channel(660427011642359811) 
      self.refreshStats.start()

    @tasks.loop(seconds=30.0)
    async def refreshStats(self):
      r = requests.get('https://teamtrees.org')
      r = r.text
      soup = BeautifulSoup(r, "html.parser")

      match = soup.find('div', class_="counter")
      treesAmount = int(match["data-count"])
      await self.treeChannel.edit(name="🎄 {0:,}".format(treesAmount))
      
      # # == TOTAL MEMBERS ==
      # # getting all members
      # allMembers = [member for member in self.bot.get_all_members()]
      # await self.totalChannel.edit(name=totalTemplate.format(len(allMembers)))


      # # == ONLINE MEMBERS ==
      # onlineMembers = 0
      # for member in allMembers:
      #   if member.status == discord.Status.online:
      #     onlineMembers+=1
      # await self.onlineChannel.edit(name=onlineTemplate.format(onlineMembers))
      
      # # == OFFLINE MEMBERS ==
      # offlineMembers = len(allMembers) - onlineMembers
      # await self.offlineChannel.edit(name=offlineTemplate.format(offlineMembers))

def setup(bot):
    print("LOADED COGS/SERVERSTATS")
    bot.add_cog(ServerStats(bot))
