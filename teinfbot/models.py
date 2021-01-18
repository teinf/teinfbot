import os
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = sqlalchemy.create_engine(os.environ.get("DATABASE_URL"), echo=False)
Base = declarative_base()


class TeinfMember(Base):
    __tablename__ = "TeinfMember"

    discordId = Column(BigInteger, primary_key=True)
    money = Column(Integer, default=300)
    exp = Column(Integer, default=0)
    timespent = Column(Integer, default=0)
    sentmessages = Column(Integer, default=0)

    def __init__(self, discord_id: int, money: int, exp: int, timespent: int, sentmessages: int):
        self.discordId = discord_id
        self.money = money
        self.exp = exp
        self.timespent = timespent
        self.sentmessages = sentmessages

    def __repr__(self):
        return f"<TeinfMember({self.discordId})>"


class Tranzakcje(Base):
    __tablename__ = "Tranzakcje"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    profit = Column(Integer)
    balance = Column(Integer)

    def __init__(self, date: datetime, profit: int, balance: int):
        self.date = date
        self.profit = profit
        self.balance = balance

    # Foreign

    discordId = Column(BigInteger, ForeignKey("TeinfMember.discordId"))
    TeinfMember = relationship("TeinfMember", back_populates="Tranzakcje")

    def __repr__(self):
        return f"<Tranzakcje({self.id}.{self.date}: {self.TeinfMember})"


TeinfMember.Tranzakcje = relationship("Tranzakcje", order_by=Tranzakcje.id, back_populates="TeinfMember")

Base.metadata.create_all(engine)
