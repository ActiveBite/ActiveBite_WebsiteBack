from flask import Blueprint
from flask_cors import cross_origin
from services.trainings_service import TrainingsService
from models.base import Session


trainings = Blueprint('trainings', __name__, url_prefix='/trainings')

trainings_service = TrainingsService()


@trainings.route('/', methods=["get"])
@cross_origin()
def get_trainings():
    # query params
    # publised=true user_id from jwt
    # favorite=true user_id from jwt
    trainings = trainings_service.get_trainings(Session=Session)
    return trainings, 200


@trainings.route('/training', methods=["get"])
@cross_origin()
def get_training_by_id():
    return 'ok', 200
