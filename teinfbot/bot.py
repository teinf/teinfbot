from discord.ext import commands
import discord

class TeinfBot(commands.Bot):
    def __init__(self, token: str, extensions):
        super().__init__(
            command_prefix=".",
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

    async def on_ready(self):
        print(
            f'\nZalogowano jako : {self.user} - {self.user.id}\nWersja: {discord.__version__}\n')