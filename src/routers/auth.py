from sqlalchemy.exc import IntegrityError
from typing import TypedDict
from flask import Blueprint, request

from models.base import Session
from services.auth_service import AuthService
from utils.validate_email import validate_email

auth = Blueprint('auth', __name__)

auth_service = AuthService()


class AuthData(TypedDict):
    username: str
    password: str


class RegData(AuthData):
    email: str


@auth.route('/authorization', methods=["POST"])
def authorization():
    try:
        user_data: AuthData = request.get_json()
        auth_service.authorization(
            Session=Session,
            username=user_data['username'],
            password=user_data['password'],
        )
        return '', 200
    except IntegrityError:
        return 'User already exist', 400
    except ValueError as e:
        print(e)
        return str(e), 400
    except KeyError:
        return 'Required params is empty', 400


@auth.route('/registration', methods=["POST"])
def registration():
    try:
        # session = Session()
        user_data: RegData = request.get_json()
        validate_email(user_data['email'])
        auth_service.registration(
            Session=Session,
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
        )
        return '', 200
    except IntegrityError:
        return 'User already exist', 400
    except ValueError as e:
        print(e)
        return str(e), 400
    except KeyError:
        return 'Required params is empty', 400
