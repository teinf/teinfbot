import psycopg2
import os

class Database:
    def __init__(self, url: str):
        try:
            self.connection = psycopg2.connect(
                url,
                sslmode='require'
                )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Error: {e}")

    def create_table(self, ids):
        with self.connection:
            table_command = "CREATE TABLE users (id varchar, money integer, exp integer, level integer)"
            self.cursor.execute(table_command)

            insert_command = "INSERT INTO users(id, money, exp, level) VALUES (%s, %s, %s, %s)"
            for id_ in ids:
                self.cursor.execute(insert_command, (str(id_), 150, 0, 1))

    def get_member(self, id_: str, *args):
        id_ = str(id_)

        getting_command = """
        SELECT * FROM users
        WHERE id=%s
        """

        self.cursor.execute(getting_command, (id_,))
        member_info = self.cursor.fetchone()

        db_names = {
            "id": member_info[0],
            "money": member_info[1],
            "exp": member_info[2],
            "level": member_info[3]
        }

        items = []
        for arg in args:
            items.append(db_names[arg])

        if len(items) == 1:
            return items[0]

        return tuple(items)

    def add_money(self, id_: str, amount: int):
        id_ = str(id_)

        money = self.get_member(id_, "money")
        money += amount

        update_command = """
        UPDATE users
        SET money=%s
        WHERE id=%s
        """

        self.cursor.execute(update_command, (money, id_))
        return money

    def add_exp(self, id_: str, amount: int):
        id_ = str(id_)

        exp, level = self.get_member(id_, "exp", "level")
        exp += amount

        exp_to_lvlup = level * 110
        if exp >= exp_to_lvlup:
            exp = abs(exp_to_lvlup - exp)
            self.add_level(id_, 1)

        update_command = """
        UPDATE users
        SET exp=%s
        WHERE id=%s
        """

        self.cursor.execute(update_command, (exp, id_))
        return exp

    def add_level(self, id_: str, amount: int):
        id_ = str(id_)

        level = self.get_member(id_, "level")
        level += amount

        update_command = """
        UPDATE users
        SET level=%s
        WHERE id=%s
        """

        self.cursor.execute(update_command, (level, id_))
        return level
