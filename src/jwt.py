import os
from flask import Request
from jose import JWTError, jwt


class JWT:
    def __call__(self, request: Request):
        if 'access_token' not in request.cookies:
            raise KeyError('Нет токена')

        token_type, token = request.cookies['auth_cookie'].split(' ')
        if token_type != 'Bearer' or not token:
            raise KeyError('Неверный тип токена')

        user_payload = self.validate_access_token(token)
        request.user_payload = user_payload

    def validate_access_token(self, access_token):
        try:
            payload = jwt.decode(
                access_token,
                key=os.getenv('JWT_ACCESS_SECRET'),
                algorithms=[os.getenv('ALGORITHM_FOR_JWT')],
            )
            if payload['user_id'] is None:
                raise self.credentials_exception
            return payload
        except JWTError:
            raise self.credentials_exception
