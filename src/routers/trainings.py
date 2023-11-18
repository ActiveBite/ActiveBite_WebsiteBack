from flask import Blueprint, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from services.trainings_service import TrainingsService
from models.base import Session


trainings = Blueprint('trainings', __name__, url_prefix='/trainings')

trainings_service = TrainingsService()


@trainings.route('/', methods=["get"])
@cross_origin()
# @jwt_required
def get_trainings():
    # query params
    # published=true, favorite=true, user_id from jwt
    published = bool(request.args.get('published'))
    favorite = bool(request.args.get('favorite'))
    print(published, 12312)
    trainings = trainings_service.get_trainings(
        Session=Session, published=published, favorite=favorite, user_id=1
    )
    return trainings, 200


@trainings.route('/a', methods=["get"])
@cross_origin()
@jwt_required
def set_training():
    trainings_service.set_training(
        Session=Session,
        title='title',
        description='desc',
        exercises=[{'exercise_id': 1, 'duration': 5}],
    )
    return 'ok', 200


@trainings.route('/training', methods=["get"])
@cross_origin()
def get_training_by_id():
    return 'ok', 200
