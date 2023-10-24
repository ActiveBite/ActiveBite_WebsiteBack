# from src.models.base import Session
from sqlalchemy.orm import sessionmaker, Session

from models.user import User


class Auth:
    def authorization():
        pass

    def registration(
        self, Session: sessionmaker[Session], username: str, email: str, password: str
    ):
        with Session() as session:
            user = User(username=username, password=password, email=email)
            session.add(user)
            session.commit()
