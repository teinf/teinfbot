import random

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import ButtonStyle

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component, ComponentContext


class Buttons(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="button", guild_ids=guild_ids)
    async def button(self, ctx: commands.Context):

        yes_button = create_button(style=ButtonStyle.green,
                                   label="Yes")
        no_button = create_button(style=ButtonStyle.red,
                                  label="No")
        action_row = create_actionrow(
            yes_button, no_button
        )

        await ctx.send(
            "Hello, World!",
            components=[
                action_row
            ]
        )

        button_ctx: ComponentContext = await wait_for_component(self.bot, components=action_row, check=lambda x: x.author_id == ctx.author.id)

        for component in action_row['components']:
            component['disabled'] = True

        await button_ctx.edit_origin(components=[action_row])

        pressedId = button_ctx.component_id
        if pressedId == yes_button['custom_id']:
            await ctx.send("Yes")
        elif pressedId == no_button['custom_id']:
            await ctx.send("No")

    @commands.command()
    async def select(self, ctx):
        await ctx.send(
            "Hello, World!",
            components=[
                Select(placeholder="select something!", options=[SelectOption(
                    label="<@367725645301678100>", value="A"), SelectOption(label="b", value="B")])
            ]
        )

        interaction = await self.bot.wait_for("select_option", check=lambda i: i.component[0].value == "A")
        await interaction.respond(content=f"{interaction.component[0].label} selected!")


def setup(bot: TeinfBot):
    bot.add_cog(Buttons(bot))
