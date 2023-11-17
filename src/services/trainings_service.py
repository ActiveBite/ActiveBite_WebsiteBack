from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select

from models.models import Training, as_list_of_dicts, favorite_training


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
            # 'select * from trainings inner join training_exercise on
            # trainings.id = training_exercise.training_id inner
            # join users on training_exercise.user_id where users.user_id = 1'
            res = session.execute(statement).all()[0]
            return as_list_of_dicts(res)

    def set_training(self):
        pass

    def delete_training(self):
        pass
