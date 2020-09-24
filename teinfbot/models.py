import sqlalchemy
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

engine = sqlalchemy.create_engine(os.environ.get("DATABASE_URL"), echo=True)
Base = declarative_base()

class TeinfMember(Base):
    __tablename__ = "TeinfMember"

    discordId = Column(BigInteger, primary_key=True)
    money     = Column(Integer)
    exp       = Column(Integer)

    def __init__(self, discordId: int, money: int, exp: int):
        self.discordId = discordId
        self.money = money
        self.exp = exp

    def __repr__(self):
        return f"<TeinfMember({self.discordId})>"


class Tranzakcje(Base):
    __tablename__ = "Tranzakcje"

    id          = Column(Integer, primary_key=True)
    bilans      = Column(Integer)
    newBalance  = Column(Integer)

    # Foreign

    discordId   = Column(BigInteger, ForeignKey("TeinfMember.discordId")) 
    TeinfMember = relationship("TeinfMember", back_populates="Tranzakcje")

    def __repr__(self):
        return f"<Tranzakcje({id} {TeinfMember.discordId})"

TeinfMember.Tranzakcje = relationship("Tranzakcje", order_by=Tranzakcje.id, back_populates="TeinfMember")


Base.metadata.create_all(engine)
