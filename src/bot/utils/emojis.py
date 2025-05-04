from typing import List

import discord


class EmojiUtils:
    @staticmethod
    def get_digits(amount=9):
        digs: List[str] = [str(i) + "\u20e3" for i in range(1, 10)]

        for digit in digs[:amount]:
            yield digit

    @staticmethod
    def get_emoji_value(emoji: discord.Emoji) -> int:
        digs: List[str] = [str(i) + "\u20e3" for i in range(1, 10)]
        return digs.index(str(emoji)) + 1

    @staticmethod
    async def add_digits(msg: discord.Message, amount: int):
        for emoji in EmojiUtils.get_digits(amount):
            await msg.add_reaction(emoji)
