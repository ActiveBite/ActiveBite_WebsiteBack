from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/authorization')
def authorization():
    pass
