import random

import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component, ComponentContext
from discord_slash.model import ButtonStyle

from teinfbot.bot import TeinfBot
from teinfbot.db import db_session
from teinfbot.models import TeinfMember
from teinfbot.utils.guilds import guild_ids


class Ruletka(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="ruletka", description="Ruletka", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="bet",
            description="Wartość zakładu",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ])
    async def __ruletka(self, ctx: SlashContext, bet: int):

        if bet <= 0:
            return

        author: TeinfMember = db_session.query(
            TeinfMember).filter_by(discordId=ctx.author.id).first()

        if author.money < bet:
            await ctx.author.send(f"Nie masz wystarczająco pieniędzy - brakuje `{abs(bet - author.money)}` chillcoinów")
            return
        else:
            author.money -= bet

        czarne = [2, 4, 6, 8, 10, 11, 13, 15, 17,
                  20, 22, 24, 26, 28, 29, 31, 33, 35]
        czerwone = [1, 3, 5, 7, 9, 12, 14, 16, 18,
                    19, 21, 23, 25, 27, 30, 32, 34, 36]

        embed = discord.Embed(
            title=f"🎰 Ruletka 🎰",
            description=f"Wybierz kolor:",
            color=discord.Color.gold()
        )

        embed.set_footer(text=f"{str(ctx.author)}",
                         icon_url=ctx.author.avatar_url)

        red_button = create_button(label="Czerwony", style=ButtonStyle.red)
        black_button = create_button(label="Czarny", style=ButtonStyle.gray)
        green_button = create_button(label="Zielony", style=ButtonStyle.green)

        action_row = create_actionrow(red_button, black_button, green_button)

        message = await ctx.send(embed=embed, components=[action_row])

        winning_number = random.randint(0, 36)
        betWinAmount = 0

        button_ctx: ComponentContext = await wait_for_component(self.bot, components=action_row, check=lambda x: x.author_id == ctx.author_id)

        for component in action_row["components"]:
            component["disabled"] = True
        await button_ctx.edit_origin(components=[action_row])

        if button_ctx.component_id == red_button["custom_id"]:
            if winning_number in czerwone:
                betWinAmount = bet * 2
        if button_ctx.component_id == black_button["custom_id"]:
            if winning_number in czarne:
                betWinAmount = bet * 2
        if button_ctx.component_id == green_button["custom_id"]:
            if winning_number == 0:
                betWinAmount = bet * 14

        desc = ""
        if winning_number in czarne:
            desc += "Czarna\n"
        elif winning_number in czerwone:
            desc += "Czerwona\n"
        elif winning_number == 0:
            desc += "Zielona"

        if betWinAmount <= 0:
            kolor = discord.Color.red()
            text = "PRZEGRAŁEŚ! \U0001F602"
        else:
            kolor = discord.Color.green()
            text = "WYGRAŁEŚ!"

        em = discord.Embed(
            title=f"\U0001F4B0 Ruletka: {ctx.message.author} \U0001F4B0", colour=kolor)
        em.add_field(
            name=f"**{text}**", value=f"Wygrywająca liczba : **{winning_number}**", inline=False)
        em.add_field(name=f"**INFO O LICZBIE**", value=desc)

        if betWinAmount > 0:
            author.money += betWinAmount
            author.exp += betWinAmount // 10
            em.add_field(name="**Profit** :",
                         value=f"**+{betWinAmount}** chillcoinsów", inline=False)

            em.set_footer(
                text=str(
                    ctx.author) + f": +{betWinAmount}CC, +{betWinAmount // 10}EXP, BILANS {author.money}",
                icon_url=ctx.author.avatar_url)
        else:
            em.set_footer(text=str(
                ctx.author) + f":BILANS {author.money}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=em)


def setup(bot: TeinfBot):
    bot.add_cog(Ruletka(bot))
