from dataclasses import dataclass
from typing import List
from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    String,
    Table,
    UniqueConstraint,
    Integer,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


def as_dict(model: Base):
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }


def as_list_of_dicts(result):
    return [as_dict(row) for row in result]


@dataclass
class Training(Base):
    __tablename__ = "trainings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text())
    description: Mapped[str] = mapped_column(String(50))
    image: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    def __repr__(self) -> str:
        return f'''Training(id={self.id}, title={self.title},
        description={self.description}, image={self.image}), user_id={self.user_id})'''


favorite_training = Table(
    'favorite_trainings',
    Base.metadata,
    Column('training_id', ForeignKey('trainings.id')),
    Column('user_id', ForeignKey('users.id')),
)


@dataclass
class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint('username', 'email'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    favorites: Mapped[List[Training]] = relationship(secondary=favorite_training)

    def __repr__(self) -> str:
        return f'''User(id={self.id}, username={self.username}, email={self.email},
        password={self.password})'''


@dataclass
class Exercise(Base):
    __tablename__ = "exercises"
    __table_args__ = (
        CheckConstraint('difficulty IN (1, 2, 3)', name="difficulty_check"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_name: Mapped[str] = mapped_column(String(255))
    difficulty: Mapped[int] = mapped_column()


training_exercise = Table(
    'training_exercises',
    Base.metadata,
    Column('training_id', ForeignKey('trainings.id')),
    Column('exercise_id', ForeignKey('exercises.id')),
    Column("duration", Integer),
)
