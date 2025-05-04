import os
import asyncio
from bot import Bot


async def main():
    tfbot = Bot(int(os.environ.get("GUILD")))
    await tfbot.run_bot()


if __name__ == "__main__":
    asyncio.run(main())
