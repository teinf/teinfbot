import discord
from discord.ext import commands

from teinfbot import db_session


class TeinfBot(commands.Bot):
    def __init__(self, token: str, extensions):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
            reconnect=True,
        )

        self.guild_id = 406476256646004736

        self.token = token

        for extension in extensions:
            try:
                self.load_extension(extension)
                print(f"[EXT] Success - {extension}")
            except commands.ExtensionNotFound:
                print(f"[EXT] Failed - {extension}")

    def run(self):
        try:
            self.loop.run_until_complete(self.bot_start())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.bot_close())

    async def bot_start(self):
        await self.login(self.token)
        await self.connect()

    async def bot_close(self):
        await super().logout()
        db_session.close()

    async def on_ready(self):
        print(
            f'\nLogged as : {self.user} - {self.user.id}\nVersion: {discord.__version__}\n')
