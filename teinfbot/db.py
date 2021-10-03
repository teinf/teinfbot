import sqlalchemy.orm
import sqlalchemy.event as event

from teinfbot.models import engine, TeinfMember, Tranzakcje, MusicHistory

Session = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=True)
db_session: sqlalchemy.orm.Session = Session()

# Podczas tworzenia bazy danych zakomentować


# @event.listens_for(TeinfMember.money, 'set', propagate=True)
# def receive_append(target: TeinfMember, value: int, oldvalue: int, initiator):
#     transaction = Tranzakcje(value - oldvalue, value)
#     target.Tranzakcje.append(transaction)
