from typing import List
import sqlite3


class Waluta:
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    @classmethod
    def update_money(cls, member_id: int, money: int):
        with cls.connection:
            cls.cursor.execute("""UPDATE users SET money = :money WHERE id = :id""", {"money": money, "id": member_id})

    @classmethod
    def update_level(cls, member_id: int, levels: int):
        with cls.connection:
            cls.cursor.execute("""UPDATE users SET level = :level WHERE id = :id""", {"level": levels, "id": member_id})

    @classmethod
    def get_member(cls, member_id: int):
        with cls.connection:
            cls.cursor.execute("SELECT * FROM user WHERE id=?", (member_id,))
        return cls.cursor.fetchone()
