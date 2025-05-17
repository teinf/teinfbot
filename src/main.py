import asyncio
from bot import Bot
from config import config


async def main():
    tfbot = Bot(config.dc.guild_id)
    await tfbot.run_bot()


if __name__ == "__main__":
    asyncio.run(main())
