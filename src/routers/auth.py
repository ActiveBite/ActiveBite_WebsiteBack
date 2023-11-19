from flask_cors import cross_origin
from typing import TypedDict
from flask import Blueprint, Response, make_response, request

from models.base import Session
from services.auth_service import AuthService
from utils.validate_email import validate_email

auth = Blueprint('auth', __name__, url_prefix='/auth')

auth_service = AuthService()


class AuthData(TypedDict):
    username: str
    password: str


class RegData(AuthData):
    email: str


@auth.route('/authorization', methods=["POST"])
@cross_origin()
def authorization():
    try:
        user_data: AuthData = request.get_json()
        info = auth_service.authorization(
            Session=Session,
            username=user_data['username'],
            password=user_data['password'],
        )
        response = make_response(info)
        response.set_cookie("access_token", value=info.pop('access_token'))
        response.set_cookie("refresh_token", value=info.pop('refresh_token'))
        return response, 200
    except ValueError as e:
        return str(e), 400
    except KeyError:
        return 'Обязательные параметры пустые', 400


@auth.route('/registration', methods=["POST"])
@cross_origin()
def registration():
    try:
        user_data: RegData = request.get_json()
        validate_email(user_data['email'])
        auth_service.registration(
            Session=Session,
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
        )
        return '', 200
    except ValueError as e:
        return str(e), 400
    except KeyError:
        return 'Обязательные параметры пустые', 400
