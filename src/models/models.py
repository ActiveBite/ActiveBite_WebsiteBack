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
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint('username', 'email'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))
    avatar: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f'''User(id={self.id}, username={self.username}, email={self.email},
        password={self.password})'''


class Train(Base):
    __tablename__ = "trains"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text())
    description: Mapped[str] = mapped_column(String(50))
    image: Mapped[str] = mapped_column(String(255))
    duration: Mapped[int] = mapped_column(Integer)


class Exercise(Base):
    __tablename__ = "exercises"
    __table_args__ = (
        CheckConstraint('difficulty IN (1, 2, 3)', name="difficulty_check"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_name: Mapped[str] = mapped_column(String(255))
    difficulty: Mapped[int] = mapped_column(Integer)


train_exercises = Table(
    "train_exercises",
    Base.metadata,
    Column("train_id", ForeignKey("trains.id")),
    Column("exercise_id", ForeignKey("exercises.id")),
    Column("exercise_duration ", Integer),
)
