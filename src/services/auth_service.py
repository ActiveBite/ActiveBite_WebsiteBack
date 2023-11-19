from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select
from passlib.hash import bcrypt
from models.models import User


class AuthService:
    def authorization(
        self, Session: sessionmaker[Session], username: str, password: str
    ):
        with Session() as session:
            statement = select(User).where(User.username == username)
            candidate = session.execute(statement).scalar_one_or_none()
            if not candidate:
                raise ValueError('Пользователь не найден')
            if not bcrypt.verify(password, candidate.password):
                raise ValueError('Неправильный пароль')
            access_token = create_access_token(
                identity=[candidate.username, candidate.id]
            )
            refresh_token = create_refresh_token(
                identity=[candidate.username, candidate.id]
            )
            info = {
                'username': candidate.username,
                'avatar': candidate.avatar,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
            return info

    def registration(
        self, Session: sessionmaker[Session], username: str, email: str, password: str
    ):
        with Session() as session:
            statement = select(User).where(User.username == username)
            candidate = session.execute(statement).scalar_one_or_none()
            if candidate:
                raise ValueError('Пользователь уже существует')
            user = User(username=username, password=bcrypt.hash(password), email=email)
            session.add(user)
            session.commit()
