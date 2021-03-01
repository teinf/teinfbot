import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter

@commands.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx: commands.Context, limit = 30, message_filter = None):

    check = None

    def is_member(msg: str):
        return msg.startswith("<@!") and msg.endswith(">")
    
    if message_filter:
        if is_member(message_filter):
            converter = MemberConverter()
            member: discord.Member = await converter.convert(ctx, message_filter)
            check = lambda m: member == m.author

        elif message_filter == "img":
            check = lambda m: m.attachments
        
        else:
            check = lambda m: message_filter in m.content
        

    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=limit, check=check)
    await ctx.channel.send('Usunięto {} wiadomości'.format(len(deleted)), delete_after=5)


def setup(bot):
    bot.add_command(clear)