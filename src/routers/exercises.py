from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import insert, select

from models.models import Exercise


class ExercisesService:
    def get_exercises(self, Session: sessionmaker[Session], search_query: str = None):
        with Session() as session:
            statement = select(Exercise)
            if search_query:
                statement.where(Exercise.exercise_name.like(f'%{search_query}%'))
            exercises = session.execute(statement.limit(5)).all()
            return exercises[0] if exercises else []
