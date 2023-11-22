# from sqlalchemy import insert
from models.base import Base, engine, Session
from services.auth_service import AuthService
from models.models import Training, favorite_training
from services.exercises_service import ExercisesService


def create_tables():
    Base.metadata.create_all(engine)
    auth = AuthService()
    auth.registration(
        Session=Session, username='tipask', password='123457', email='tttt@ya.ru'
    )
    exercise_service = ExercisesService()
    exercises = [{
        'name': 'Становая тяга',
        'difficulty': 3
    },{
        'name': 'Скручивания на пресс',
        'difficulty': 1
    },{
        'name': 'Румынская тяга',
        'difficulty': 3
    },{
        'name': 'Выпады со штангой',
        'difficulty': 2
    },{
        'name': 'Подтягивания на перекладине',
        'difficulty': 1
    }]
    for exercise in exercises:
        exercise_service.set_exercise(Session=Session, exercise_name=exercise['name'],
                                      difficulty=exercise['difficulty'])
    training = Training(title='training', description='asdadadads')
    with Session() as session:
        session.add(training)
        # stmnt = insert(favourite_training).values(training)
        session.execute(favorite_training.insert().values(training_id=1, user_id=1))
        session.commit()


def drop_tables():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_tables()
