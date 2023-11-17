from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///test.db", echo=True)

Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
