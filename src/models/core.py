from sqlalchemy import insert
from models.base import Base, engine, Session
from services.auth_service import AuthService
from models.models import Training, User, favorite_training


def create_tables():
    Base.metadata.create_all(engine)
    auth = AuthService()
    auth.registration(
        Session=Session, username='tipask', password='123457', email='tttt@ya.ru'
    )
    # print(auth.authorization(Session=Session, username='tipask', password='123457'))
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
