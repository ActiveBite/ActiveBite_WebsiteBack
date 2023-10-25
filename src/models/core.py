from models.base import Base, engine, Session
from services.auth_service import AuthService


def create_tables():
    Base.metadata.create_all(engine)
    auth = AuthService()
    auth.registration(Session=Session, username='tipask', password='123457', email='tttt@ya.ru')
    print(auth.authorization(Session=Session, username='tipask', password='123457'))


def drop_tables():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_tables()
