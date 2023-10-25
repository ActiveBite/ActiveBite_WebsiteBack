# from src.models.base import Session
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select
from passlib.hash import bcrypt
from models.user import User


class AuthService:
    def authorization(
        self, Session: sessionmaker[Session], username: str, password: str
    ):
        with Session() as session:
            statement = select(User).where(User.username == username)
            candidate = session.execute(statement).scalar_one_or_none()
            if not candidate:
                raise ValueError('Not found')
            if not bcrypt.verify(password, candidate.password):
                raise ValueError('Wrong password')
            return 'ok'

    def registration(
        self, Session: sessionmaker[Session], username: str, email: str, password: str
    ):
        with Session() as session:
            statement = select(User).where(User.username == username)
            candidate = session.execute(statement).scalar_one_or_none()
            if candidate:
                raise ValueError('Already exist')
            user = User(username=username, password=bcrypt.hash(password), email=email)
            session.add(user)
            session.commit()
