from typing import Literal
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import and_, insert, select

from models.models import (
    Exercise,
    Training,
    as_dict,
    as_list_of_dicts,
    favorite_training,
    training_exercise,
    training_likes,
    training_dislikes
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

    def get_training_by_id(self, Session: sessionmaker[Session], training_id: int, user_id: int):
        with Session() as session:
            select_training = select(Training).where(Training.id == training_id)
            select_exercises = select(Exercise).join(
                training_exercise, onclause=Exercise.id == training_exercise.c.exercise_id
            ).where(training_exercise.c.training_id == training_id)

            training = session.execute(select_training).scalar()
            exercises = session.execute(select_exercises).all()
            liked = session.execute(
                training_likes.select().where(
                    and_(training_likes.c.training_id == training_id, training_likes.c.user_id == user_id)
                )
            ).one_or_none()
            disliked = session.execute(
                training_dislikes.select().where(
                    and_(training_dislikes.c.training_id == training_id, training_dislikes.c.user_id == user_id)
                )
            ).one_or_none()

            training_dict = as_dict(training)
            exercise_list = as_list_of_dicts(exercises)

            training_info = {
                'training': training_dict,
                'exercises': exercise_list,
                'like': bool(liked),
                'dislike': bool(disliked),
                'favorite': False
            } if training else {}
            print(training_info)
            return training_info

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

    def rate_training(self, Session: sessionmaker[Session], training_id: int,
                      user_id: int, rate: Literal['like', 'dislike']):
        with Session() as session:
            target_table = training_likes if rate == 'like' else training_dislikes

            session.execute(
                training_likes.delete().where(
                    and_(training_likes.c.training_id == training_id, training_likes.c.user_id == user_id)
                )
            )
            session.execute(
                training_dislikes.delete().where(
                    and_(training_dislikes.c.training_id == training_id, training_dislikes.c.user_id == user_id)
                )
            )

            session.execute(
                target_table.insert().values(
                    training_id=training_id, user_id=user_id
                )
            )

            session.commit()

    def add_to_favorite(self, Session: sessionmaker[Session], training_id: int, user_id: int):
        with Session() as session:
            is_training_exists = session.execute(
                favorite_training.select().where(
                    and_(favorite_training.c.training_id == training_id, favorite_training.c.user_id == user_id)
                )
            )
            if is_training_exists:
                session.execute(
                    favorite_training.delete().where(
                        and_(favorite_training.c.training_id == training_id, favorite_training.c.user_id == user_id)
                    )
                )
            else:
                session.execute(favorite_training.insert().values(training_id, user_id))

    def delete_training(self):
        pass
