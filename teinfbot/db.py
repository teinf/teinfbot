import sqlalchemy.orm

from teinfbot.models import engine

Session = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=True)
db_session: sqlalchemy.orm.Session = Session()

print("DB LOADED")

# Podczas tworzenia bazy danych zakomentować
# @event.listens_for(TeinfMember.money, 'set', propagate=True)
# def receive_append(target: TeinfMember, value: int, oldvalue: int, initiator):
#     transaction = Tranzakcje(datetime.now(), value - oldvalue, value)
#     target.Tranzakcje.append(transaction)
