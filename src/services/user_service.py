from sqlalchemy import or_, select
from sqlalchemy.orm import sessionmaker, Session

from models.models import User


class UserService:
    def get_user(
        self, Session: sessionmaker[Session], username: str = None, user_id: str = None
    ):
        if not username and not user_id:
            raise ValueError('username or user_id required')
        with Session() as session:
            statement = select(User).where(
                or_(User.id == user_id, User.username == username)
            )
            user = session.execute(statement)
            return user

    def add_favorite_training(self, Session: sessionmaker[Session], user_id: int):
        with Session() as session:
            pass
