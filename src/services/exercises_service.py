from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import insert, select

from models.models import Exercise, as_list_of_dicts


class ExercisesService:
    def get_exercises(self, Session: sessionmaker[Session], search_query: str = None):
        with Session() as session:
            statement = select(Exercise)
            if search_query:
                statement.where(Exercise.exercise_name.like(f'%{search_query}%'))
            exercises = session.execute(statement).all()
            print(exercises)
            return as_list_of_dicts(exercises) if exercises else []
        
    def set_exercise(self, Session: sessionmaker[Session], exercise_name: str, difficulty: int):
        with Session() as session:
            new_exercise = Exercise(exercise_name=exercise_name, difficulty=difficulty)
            session.add(new_exercise)
            session.commit()
