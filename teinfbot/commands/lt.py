import random

import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component, ComponentContext
from discord_slash.model import ButtonStyle


from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids


class Lt(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="lt", guild_ids=guild_ids, description="Wylosowanie teamów", options=[
        manage_commands.create_option(
            name="ilosc_druzyn",
            description="Ilość drużyn do losowania teamu",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ])
    async def __lt(self, ctx: SlashContext, ilosc_druzyn: int):

        author = ctx.author  # osoba która wywołała komende

        em = discord.Embed(
            title=":star2: LOSOWANIE TEAMU :star2:",
            description="ABY **DOŁĄCZYĆ** :white_check_mark:\n**KONIEC** CZEKANIA :x:",
            colour=discord.Colour.gold()
        )
        join_button = create_button(
            style=ButtonStyle.green, label="Dołącz", emoji="\u2705")
        leave_button = create_button(
            style=ButtonStyle.danger, label="Wyjdź", emoji="⛔")
        end_button = create_button(
            style=ButtonStyle.gray, label="Losuj", emoji="🎲")

        action_row = create_actionrow(join_button, leave_button, end_button)

        message = await ctx.send(embed=em, components=[action_row])
        users = []

        while True:
            button_ctx: ComponentContext = await wait_for_component(self.bot, components=action_row)
            if button_ctx.component_id == join_button["custom_id"]:
                if button_ctx.author not in users:
                    users.append(button_ctx.author)
            elif button_ctx.component_id == leave_button["custom_id"]:
                if button_ctx.author in users:
                    users.remove(button_ctx.author)

            elif button_ctx.component_id == end_button["custom_id"] and button_ctx.author_id == ctx.author_id:
                await button_ctx.edit_origin(embed=em)
                break

            em = discord.Embed(
                title=":star2: LOSOWANIE TEAMU :star2:",
                description=f"Gracze: {', '.join((user.mention for user in users))}",
                colour=discord.Colour.gold()
            )

            await button_ctx.edit_origin(embed=em)

        random.shuffle(users)

        teams: List[discord.User] = []
        for i in range(1, ilosc_druzyn + 1):
            teams.append(users[i - 1::ilosc_druzyn])

        message = await ctx.channel.fetch_message(message.id)
        await message.delete()  # usuwanie wcześniej wysłanych wiadomości

        for i, team in enumerate(teams):
            color = discord.Color.random()

            team_users = ""
            for userNumber, user in enumerate(team, start=1):
                team_users += f"{userNumber}. {user.mention}\n"

            team_embed = discord.Embed(
                title=f"TEAM {i + 1}", description=team_users, colour=color)

            await ctx.channel.send(embed=team_embed)


def setup(bot: TeinfBot):
    bot.add_cog(Lt(bot))
