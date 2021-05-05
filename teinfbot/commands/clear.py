import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands

from teinfbot.bot import TeinfBot
from teinfbot.utils.guilds import guild_ids


class Clear(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot: TeinfBot = bot

    @cog_ext.cog_slash(name="clear", description="Usuwanie wiadomości", guild_ids=guild_ids)
    async def __clear(self, ctx: SlashContext):
        
        deleted = await ctx.channel.purge(limit=10)
        await ctx.channel.send('Usunięto {} wiadomości'.format(len(deleted)), delete_after=5)
    
    @cog_ext.cog_subcommand(base="clear", name="default",  description="Domyślne usuwanie wiadomości", guild_ids=guild_ids, options=[
            manage_commands.create_option(
                name="limit",
                description="Ilośc wiadomości do przeszukania",
                option_type=SlashCommandOptionType.INTEGER,
                required=True
            ),
        ]   
    )
    async def __clear_text(self, ctx: SlashContext, limit: int):
        
        deleted = await ctx.channel.purge(limit=limit)
        await ctx.channel.send('Usunięto {} wiadomości'.format(len(deleted)), delete_after=5)

    @cog_ext.cog_subcommand(base="clear", name="text", description="Usuwanie wiadomości na podstawie tekstu", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="limit",
            description="Ilośc wiadomości do przeszukania",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        ),
        manage_commands.create_option(
            name="text",
            description="Filtr wiadomości",
            option_type=SlashCommandOptionType.STRING,
            required=True
        )
    ]
                            )
    async def __clear_text(self, ctx: SlashContext, limit: int, text: str):
        
        deleted = await ctx.channel.purge(limit=limit, check=lambda msg: text in msg.content)
        await ctx.channel.send('Usunięto {} wiadomości'.format(len(deleted)), delete_after=5)

    @cog_ext.cog_subcommand(base="clear", name="media",  description="Usuwanie zdjęć/filmików", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="limit",
            description="Ilośc wiadomości do przeszukania",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        ),
    ]
                            )
    async def __clear_media(self, ctx: SlashContext, limit: int, text: str):
        
        deleted = await ctx.channel.purge(limit=limit, check=lambda msg: msg.attachments)
        await ctx.channel.send('Usunięto {} wiadomości'.format(len(deleted)), delete_after=5)

    @cog_ext.cog_subcommand(base="clear", name="user", description="Usuwanie wiadomości użytkownika", guild_ids=guild_ids, options=[
        manage_commands.create_option(
            name="limit",
            description="Ilośc wiadomości do przeszukania",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        ),
        manage_commands.create_option(
            name="user",
            description="Wiadomości użytkownika które zostaną usunięte",
            option_type=SlashCommandOptionType.USER,
            required=True
        ),

    ]
                            )
    async def __clear_user(self, ctx: SlashContext, limit: int, user: discord.Member):
        
        deleted = await ctx.channel.purge(limit=limit, check=lambda msg: user == msg.author)
        await ctx.channel.send('Usunięto {} wiadomości'.format(len(deleted)), delete_after=5)


def setup(bot: TeinfBot):
    bot.add_cog(Clear(bot))
