from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import insert, select

from models.models import (
    Exercise,
    Training,
    as_dict,
    as_list_of_dicts,
    favorite_training,
    training_exercise,
)


class TrainingsService:
    def get_trainings(
        self,
        Session: sessionmaker[Session],
        user_id: int = None,
        published: bool = None,
        favorite: bool = None,
    ):
        with Session() as session:
            if published:
                statement = select(Training).where(Training.user_id == user_id)
            elif favorite:
                statement = (
                    select(Training)
                    .join(
                        favorite_training,
                        onclause=Training.id == favorite_training.c.training_id,
                    )
                    .where(favorite_training.c.user_id == user_id)
                )
            else:
                statement = select(Training)
            res = session.execute(statement).all()
            if not res:
                return []
            return as_list_of_dicts(res)

    def get_training_by_id(self, Session: sessionmaker[Session], training_id: int):
        with Session() as session:
            select_training = select(Training).where(Training.id == training_id)
            select_exercises = select(Exercise).join(training_exercise,
                                                     onclause=Exercise.id == training_exercise.c.exercise_id).where(training_exercise.c.training_id == training_id)
            training = session.execute(select_training).scalar()
            exercises = session.execute(select_exercises).all()
            training_dict = as_dict(training)
            exercise_list = as_list_of_dicts(exercises)
            return {'training': training_dict, 'exercises': exercise_list} if training else {}

    def set_training(
        self,
        Session: sessionmaker[Session],
        title: str,
        description: str,
        exercises: list[dict[str, int]],
        img: str | None = None,
        user_id: int | None = None,
    ):
        with Session() as session:
            new_training = Training(
                title=title, description=description, image=img, user_id=user_id
            )
            session.add(new_training)
            session.flush()
            for exercise in exercises:
                exercise['training_id'] = new_training.id
            insert_exercises = insert(training_exercise).values(exercises)
            print(new_training.id)
            session.execute(insert_exercises)
            session.commit()

    def set_exercise(self, Session: sessionmaker[Session], exercise_name, difficulty):
        with Session() as session:
            new_exercise = Exercise(exercise_name=exercise_name, difficulty=difficulty)
            session.add(new_exercise)
            session.commit()

    def delete_training(self):
        pass
