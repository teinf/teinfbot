from sqlalchemy.orm import sessionmaker
from teinfbot.models import engine, TeinfMember, Tranzakcje

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()