from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from teinfbot.models import engine, TeinfMember, Tranzakcje

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()


@event.listens_for(TeinfMember.money, 'set', propagate=True)
def receive_append(target: TeinfMember, value: int, oldvalue: int, initiator):
    transaction = Tranzakcje(value - oldvalue, value)
    target.Tranzakcje.append(transaction)