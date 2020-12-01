import asyncio

from discord.ext import commands
import discord
from teinfbot import db
from teinfbot import TeinfBot
from teinfbot.models import TeinfMember
from typing import List
import random


class Poker(commands.Cog):
    def __init__(self, bot: TeinfBot):
        self.bot = bot

    async def send_entry_message(self, ctx, bet_amount) -> discord.Message:
        entry_embed = discord.Embed(
            title="Poker",
            description=f"Czy podejmiesz się wyzwaniu?\nKliknij 🎲 aby dołączyć\n🏁 aby wystartować\nKoszt wstępu: `{bet_amount}` chillcoinsów",
            color=discord.Color.red()
        )

        entry_message: discord.Message = await ctx.send(embed=entry_embed)
        await entry_message.add_reaction("🎲")
        await entry_message.add_reaction("🏁")

        return entry_message

    async def wait_for_emoji(self, ctx, message: discord.Message, emoji: str, wait_time: int = 120):
        try:
            await self.bot.wait_for(
                "reaction_add",
                check=lambda react, usr: usr == ctx.author and str(
                    react.emoji) == emoji and react.message.id == message.id,
                timeout=wait_time
            )
        except asyncio.TimeoutError:
            return False

        return True

    async def get_users_by_emoji_from_message(self, ctx: commands.Context, message: discord.Message, emoji: str) -> List[discord.Member]:

        message = await ctx.fetch_message(message.id)
        reactions: List[discord.Reaction] = message.reactions
        reaction_emoji = [reaction for reaction in reactions if reaction.emoji == emoji][0]

        users = [user for user in await reaction_emoji.users().flatten() if
                                 user.display_name != self.bot.user.display_name]

        return users

    @commands.command(name="poker.start")
    async def poker_start(self, ctx: commands.Context, bet_amount: int):

        entry_message = await self.send_entry_message(ctx, bet_amount)
        if not await self.wait_for_emoji(ctx, entry_message, "🏁"):
            return

        deck = Deck(size=2)
        deck.shuffle_deck()

        players = await self.get_users_by_emoji_from_message(ctx, entry_message, "🎲")
        players = [PokerPlayer(player, deck.cards.pop(0), deck.cards.pop(0)) for player in players]

        for player in players:
            await player.discordMember.send(f"Pierwsza karta: {player.firstCard}\nDruga karta {player.secondCard}")

        STARTING_CARDS_ON_TABLE = 3
        table_cards = [deck.cards.pop(0) for _ in range(STARTING_CARDS_ON_TABLE)]

        cards_desc = "  ".join((str(card) for card in table_cards))
        table_message_embed = discord.Embed(
            title="Stół",
            description=cards_desc,
            color=discord.Color.green()
        )

        table_message: discord.Message = await ctx.channel.send(embed=table_message_embed)

        current_bet = bet_amount

        ROUNDS_AMOUNT = 3
        for round in range(ROUNDS_AMOUNT):
            # Proszenie o bet, raise, fold
            for player in players:
                choice_message = await ctx.channel.send(f"Obecny bet `{current_bet}`\n1.")





class Card:
    colors = {
        "hearts": ":hearts:",
        "spades": ":spades:",
        "clubs": ":clubs:",
        "diamonds": ":diamonds:"
    }

    values = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")

    def __init__(self, value, color):
        self.value = value
        self.color = color

    @staticmethod
    def get_random_card():
        return Card(Card.colors[random.choice(Card.colors)], random.choice(Card.values))

    def __repr__(self):
        return self.value + self.color


class Deck:
    def __init__(self, size):
        self.cards = Deck.generate_deck(size)

    @staticmethod
    def generate_deck(size=1):
        cards: List[Card] = []

        for s in range(size):
            for color in Card.colors:
                for value in Card.values:
                    card = Card(value, Card.colors[color])
                    cards.append(card)

        return cards

    def shuffle_deck(self):
        random.shuffle(self.cards)

class PokerPlayer:
    def __init__(self, discordMember: discord.Member, firstCard, secondCard):
        self.secondCard = secondCard
        self.firstCard = firstCard
        self.discordMember = discordMember
        self.TeinfMember = db.session.query(TeinfMember).filter_by(discordId=discordMember.id).first()

def setup(bot):
    bot.add_cog(Poker(bot))
