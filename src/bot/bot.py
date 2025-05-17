import os
import discord
from discord.ext import commands
from discord import app_commands
from config import config

SRC = os.path.join("src")
BOT_SRC = os.path.join(SRC, "bot")
COMMANDS_PATH = os.path.join(BOT_SRC, "commands")
TASKS_PATH = os.path.join(BOT_SRC, "tasks")
EVENTS_PATH = os.path.join(BOT_SRC, "events")


class Bot(commands.Bot):
    def __init__(self, guild_id: int):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
            reconnect=True,
        )

        self.guild = discord.Object(id=guild_id)

    async def setup_hook(self):
        await self.retrieve_extensions()
        await self.tree.sync(guild=self.guild)

    async def run_bot(self):
        async with self:
            await self.start(config.bot.access_token)

    async def retrieve_extensions(self):
        print("Loading  extensions")

        async def addExtension(path, prefix):
            EXTS = [
                ext.split(".")[0] for ext in os.listdir(path) if ext.endswith(".py")
            ]
            print("\n" + f"LOADING {prefix.upper()}" + "\n")
            for ext in EXTS:
                try:
                    ext_fullname = "bot." + prefix + "." + ext
                    await self.load_extension(ext_fullname)
                    print(f"[{prefix.upper()}] Success - {ext}")
                except Exception:
                    print(f"[{prefix.upper()}] Failed - {ext}")
                    raise

        await addExtension(COMMANDS_PATH, "commands")
        await addExtension(TASKS_PATH, "tasks")
        await addExtension(EVENTS_PATH, "events")

    async def on_ready(self):
        print(
            f"\nLogged in as : {self.user} - {self.user.id}\nVersion: {discord.__version__}\n"
        )

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        # Log the error (optional)
        print(f"Error in command {interaction.command.name}: {error}")

        # Inform the user (optional)
        if interaction.response.is_done():
            await interaction.followup.send(
                "Wystąpił błąd podczas wykonywania komendy.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Wystąpił błąd podczas wykonywania komendy.", ephemeral=True
            )

    async def get_members_in_voice_channels(self) -> list[discord.Member]:
        AFK_CHANNEL_ID = 423934688244006913
        members = []
        for channel in self.get_all_channels():
            if str(channel.type) == "voice" and channel.id != AFK_CHANNEL_ID:
                members.extend(channel.members)
        return members
