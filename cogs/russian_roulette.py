import discord
from discord.ext import commands
import asyncio
from typing import List, Tuple
import random
import utils


class Russian(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def players_description(self, players):
        desc = "\n"
        for i, player in enumerate(players, start=1):
            desc += f"{i}. {str(player.member)}\n"
        return desc

    async def handle_reactions(self, ctx: commands.Context, msg: discord.Message, player: discord.Member):
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check=lambda react, usr: react.message.id == msg.id and usr == player,
                timeout=30
            )

            kill_decision = utils.get_emoji_value(reaction.emoji)
            return kill_decision
        except asyncio.TimeoutError:
            # Gdy nie zdąży dodać reakcji - 30 sekund
            await ctx.send(embed=discord.Embed(
                title="⏰ Upływ czasu ⏰",
                description=f"{player.mention} nie zdążył strzelić!\nZa kare dostał kulkę od barmana",
                color=discord.Color.red()
            ))
            return -1

    @commands.command(name="rr")
    async def rr(self, ctx: commands.Context, stawka: int):
        if stawka <= 0:
            return

        start_embed = discord.Embed(
            title="Rosyjska ruletka",
            description=f"Czy podejmiesz się wyzwaniu?\nKliknij 🔫 aby dołączyć\n🏁 aby wystartować\nKoszt wstępu: `{stawka}` chillcoinsów",
            color=discord.Color.red()
        )

        start_embed.set_image(url=self.bot.user.avatar_url)
        start_embed.set_footer(text=f"Komenda wyłołana przez {ctx.author.name}", icon_url=ctx.author.avatar_url)

        start_message: discord.Message = await ctx.send(embed=start_embed)
        await start_message.add_reaction("🔫")
        await start_message.add_reaction("🏁")

        try:
            await self.bot.wait_for(
                "reaction_add",
                check=lambda react, usr: usr == ctx.author and str(
                    react.emoji) == "🏁" and react.message.id == start_message.id,
                timeout=120
            )
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(
                title="Upływ czasu",
                description=f"Upłynął czas na dodanie 🏁 przez {ctx.author.name}",
                color=discord.Color.red()
            ), delete_after=20)
            await start_message.delete()

        start_message: discord.Message = await ctx.fetch_message(start_message.id)

        players: List[Player] = [Player(player) for player in await start_message.reactions[0].users().flatten() if
                                 player.display_name != self.bot.user.display_name]

        if len(players) <= 1:
            return

        for player in players:
            money = self.bot.db.get_member(player.id, "money")
            if money < stawka:
                players.remove(player)
                await player.member.send(
                    "Niestety nie możesz zagrać w rosyjską ruletkę - masz za mało pieniędzy! - {}".format(money))
            else:
                self.bot.db.add_money(player.id, stawka)
        print(players)
        if len(players) <= 1:
            return

        random.shuffle(players)

        start_players_amount = len(players)
        revolver = Gun(ctx)
        while len(players) > 1:
            for player in players:
                embed = discord.Embed(
                    title="🤔 Wybór 🤔",
                    description=f"{player.member.mention}\n1. Strzał w siebie\n2. Strzał w innego",
                    color=discord.Color.purple()
                )

                embed.set_footer(text=f"{str(player.member)}", icon_url=player.member.avatar_url)

                msg = await ctx.send(embed=embed, delete_after=20)
                await utils.add_digits(msg, 2)

                kill_decision = await self.handle_reactions(ctx, msg, player.member)

                if kill_decision == -1:
                    players.remove(player)

                elif kill_decision == 1:
                    # strzelanie w siebie
                    target = player
                    target_killed = await player.shot(ctx, target, revolver, self_shot=True)
                    if target_killed:
                        players.remove(target)

                elif kill_decision == 2:
                    message = await ctx.send(embed=discord.Embed(
                        title="Strzał!",
                        description=f"{player.member.mention} wybierz osobę w którą chcesz strzelić" + self.players_description(
                            players),
                        color=discord.Color.green()
                    ))

                    await utils.add_digits(message, len(players))
                    response = await self.handle_reactions(ctx, message, player.member)

                    target = players[response - 1]
                    target_killed = await player.shot(ctx, target, revolver)

                    if not target_killed:
                        await ctx.send(embed=discord.Embed(
                            title="Strzał w siebie",
                            description=f"{player.member.mention} niestety teraz musisz strzelać do siebie...",
                            color=discord.Color.red()
                        ))

                        target = player
                        target_killed = await player.shot(ctx, target, revolver, self_shot=True)
                        if target_killed:
                            players.remove(target)

                    else:
                        players.remove(target)

        winning_player = players[0]

        embed = discord.Embed(
            title="🏆 Wygrana! 🏆",
            description=f"Gratulacje {winning_player} wygrałeś rozgrywkę!",
            color=discord.Color.green()
        )

        money_gained = start_players_amount * stawka
        exp_gained = money_gained // 2
        embed.set_footer(text=f"+{money_gained}cc, +{exp_gained}exp")
        await ctx.send(embed=embed)
        self.bot.db.add_money(winning_player.id, money_gained)
        self.bot.db.add_exp(winning_player.id, exp_gained)


class Gun:
    def __init__(self, ctx: commands.Context, ammo_count: int = 6, bullets_count: int = 1):
        self.ammo_count = ammo_count
        self.bullets_count = bullets_count
        self.ammo = self.create_ammo()
        self.index = 0
        self.ctx = ctx

    def create_ammo(self) -> List[bool]:
        ammo = []
        for _ in range(self.ammo_count - self.bullets_count):
            ammo.append(False)
        for _ in range(self.bullets_count):
            ammo.append(True)

        random.shuffle(ammo)
        return ammo

    @property
    def current_ammo(self):
        return self.ammo[self.index]

    async def spin(self):
        self.ammo = self.create_ammo()
        self.index = 0

        await self.ctx.send(embed=discord.Embed(
            title="Przeładowanie",
            description="Umieszczenie naboju do jednej z komór...",
            color=discord.Color.orange()
        ))

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.ammo):
            raise StopIteration

        tmp_index = self.index
        self.index += 1
        return self.ammo[tmp_index]


class Player:
    def __init__(self, member: discord.Member):
        self.member = member
        self.id = self.member.id

    def __repr__(self):
        return str(self.member)

    async def shot(self, ctx: commands.Context, other, gun: Gun, self_shot: bool = False):
        try:
            bullet_inside = next(gun)
        except StopIteration:
            await gun.spin()
            bullet_inside = next(gun)

        if bullet_inside and not self_shot:
            embed = discord.Embed(
                title="☠ ŚMIERĆ ☠",
                description=f"Niestety umarł {str(other.member)}\nZostał zabity przez {str(self.member)}",
                color=discord.Color.red()
            )

            embed.set_footer(text=self.member.display_name, icon_url=self.member.avatar_url)

            await ctx.send(embed=embed)
            await gun.spin()

        elif bullet_inside and self_shot:
            embed = discord.Embed(
                title="☠ ŚMIERĆ ☠",
                description=f"Niestety umarł {str(other.member)}\nPopełnił on samobójstwo",
                color=discord.Color.red()
            )

            embed.set_footer(text=self.member.display_name, icon_url=self.member.avatar_url)

            await ctx.send(embed=embed)
            await gun.spin()

        elif not bullet_inside:

            embed = discord.Embed(
                title="💉 PRZEŻYŁ 💉",
                description=f"{str(other.member)} Przeżył\nStrzał {str(self.member)} nie miał kuli!",
                color=discord.Color.green()
            )
            embed.set_footer(text=self.member.display_name, icon_url=self.member.avatar_url)

            await ctx.send(embed=embed, delete_after=10)

        return bullet_inside


def setup(bot):
    bot.add_cog(Russian(bot))
