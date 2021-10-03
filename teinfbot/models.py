import os
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, BigInteger, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

DEBUG = True if os.environ.get("DEBUG") == "TRUE" else False
DATABASE_URL = ""
if DEBUG:
    DATABASE_URL = os.environ.get("DEBUG_DATABASE_URL")
else:
    DATABASE_URL = os.environ.get("DATABASE_URL")

engine = sqlalchemy.create_engine(DATABASE_URL, echo=False)
Base = declarative_base()


class TeinfMember(Base):
    __tablename__ = "TeinfMember"

    discordId = Column(BigInteger, primary_key=True)
    money = Column(Integer, default=300)
    exp = Column(Integer, default=0)
    timespent = Column(Integer, default=0)
    sentmessages = Column(Integer, default=0)

    def __init__(self, discord_id: int, money: int = 300, exp: int = 0, timespent: int = 0, sentmessages: int = 0):
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
    date = Column(DateTime, default=datetime.datetime.utcnow)
    profit = Column(Integer)
    balance = Column(Integer)

    def __init__(self, profit: int, balance: int):
        self.profit = profit
        self.balance = balance

    # Foreign

    discordId = Column(BigInteger, ForeignKey("TeinfMember.discordId"))
    TeinfMember = relationship("TeinfMember", back_populates="Tranzakcje")

    def __repr__(self):
        return f"<Tranzakcje({self.id}.{self.date}: {self.TeinfMember})"


class MusicHistory(Base):
    __tablename__ = "MusicHistory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    played_at = Column(DateTime, default=datetime.datetime.utcnow)
    discordId = Column(BigInteger)
    url = Column(Text)
    source = Column(Text)

    def __init__(self, discordId: int, url: str, source: str):
        self.discordId = discordId
        self.url = url
        self.source = source


TeinfMember.Tranzakcje = relationship(
    "Tranzakcje", order_by=Tranzakcje.id, back_populates="TeinfMember")

Base.metadata.create_all(engine)
