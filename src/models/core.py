# from sqlalchemy import insert
from models.base import Base, engine, Session
from services.auth_service import AuthService
from models.models import Training, favorite_training
from services.exercises_service import ExercisesService
from services.trainings_service import TrainingsService


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
    trainings_service = TrainingsService()
    trainings_service.set_training(
        Session=Session,
        title='Тест тренировка',
        description='Тест описание тест описание тест описание тест описание тест описание тест описание',
        exercises=[{'exercise_id': 1, 'duration': 5}, {'exercise_id': 1, 'duration': 15}],
    )


def drop_tables():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_tables()
