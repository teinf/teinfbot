import discord

from teinfbot.utils.music import YTDLSource


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Teraz gram',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blue())
                 .add_field(name='Czas trwania', value=self.source.duration)
                 .add_field(name='Włączone przez', value=self.requester.mention)
                 .add_field(name='URL', value='[Kliknij]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))
        return embed
