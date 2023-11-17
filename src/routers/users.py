from flask import Blueprint

# from flask_cors import cross_origin


users = Blueprint('users', __name__, url_prefix='/users')
