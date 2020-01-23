import sqlite3
import discord
import os


class Baza:
    connection = sqlite3.connect("discord_users.db")
    cursor = connection.cursor()
    kolumny = {
        "id": 0,
        "money": 1,
        "exp": 2,
        "level": 3
    }

    # SETTERS
    @classmethod
    def set_money(cls, member_id: int, money: int):
        with cls.connection:
            cls.cursor.execute("""UPDATE users SET money = :money WHERE id = :id""", {"money": money, "id": member_id})

    @classmethod
    def set_exp(cls, member_id: int, exp: int):
        with cls.connection:
            cls.cursor.execute("""UPDATE users SET exp = :exp WHERE id = :id""", {"exp": exp, "id": member_id})

    @classmethod
    def set_level(cls, member_id: int, levels: int):
        with cls.connection:
            cls.cursor.execute("""UPDATE users SET level = :level WHERE id = :id""", {"level": levels, "id": member_id})

    # GETTERS

    @classmethod
    def get_member(cls, member_id: int):
        with cls.connection:
            cls.cursor.execute("SELECT * FROM users WHERE id=?", (member_id,))
        return cls.cursor.fetchone()[cls.kolumny["id"]]

    @classmethod
    def get_money(cls, member_id: int):
        with cls.connection:
            cls.cursor.execute("SELECT * FROM users WHERE id=?", (member_id,))
        return cls.cursor.fetchone()[cls.kolumny["money"]]

    @classmethod
    def get_exp(cls, member_id: int):
        with cls.connection:
            cls.cursor.execute("SELECT * FROM users WHERE id=?", (member_id,))
        return cls.cursor.fetchone()[cls.kolumny["exp"]]

    @classmethod
    def get_level(cls, member_id: int):
        with cls.connection:
            cls.cursor.execute("SELECT * FROM users WHERE id=?", (member_id,))
        return cls.cursor.fetchone()[cls.kolumny["level"]]

    # ADDERS

    @classmethod
    def add_money(cls, member_id: int, amount: int):
        with cls.connection:
            money = cls.get_money(member_id)
            money += amount
            cls.set_money(member_id, money)

    @classmethod
    def add_exp(cls, member_id: int, amount: int):
        with cls.connection:
            exp = cls.get_exp(member_id)
            level = cls.get_level(member_id)

            overflow = (exp + amount) - (level * 1.1 * 100)
            overflow = int(overflow)
            if overflow >= 0:
                cls.add_level(member_id, 1)
                cls.set_exp(member_id, overflow)
            else:
                cls.set_exp(member_id, exp + amount)

    @classmethod
    def add_level(cls, member_id: int, amount: int):
        with cls.connection:
            level = cls.get_level(member_id)
            level += amount
            cls.set_level(member_id, level)

    # RANKING

    @classmethod
    def get_top(cls, amount: int):
        cls.cursor.execute("SELECT * FROM users")
        all_users = cls.cursor.fetchall()
        all_users.sort(key=lambda x: x[cls.kolumny["money"]])
        return all_users


# if __name__ == "__main__":
#     bot = discord.Client()
#
#
#     @bot.event
#     async def on_ready():
#         connection = sqlite3.connect("discord_users.db")
#         connection.execute("CREATE TABLE users (id integer, money integer, exp integer, level integer)")
#
#         cursor = connection.cursor()
#
#         guild: discord.Guild = bot.get_guild(406476256646004736)
#         x = [member for member in guild.members if not member.bot]
#
#         with connection:
#             for member in x:
#                 cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (member.id, 300, 0, 1))
#
#
#     bot.run(os.environ["ACCESS_TOKEN"])
