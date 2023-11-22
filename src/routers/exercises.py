from flask import Blueprint, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from models.base import Session
from services.exercises_service import ExercisesService


exercises = Blueprint('exercises', __name__, url_prefix='/exercises')

exercises_service = ExercisesService()


@exercises.route('/', methods=["get"])
@jwt_required
def get_exercises():
    search_query = request.get_json('search_query')
    exercises = exercises_service.get_exercises(
        Session=Session, search_query=search_query
    )
    return exercises
