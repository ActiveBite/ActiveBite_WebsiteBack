from flask import Blueprint
from flask_cors import cross_origin
from services.trains_service import TrainsService


trains = Blueprint('trains', __name__, url_prefix='/trains')

trains_service = TrainsService()


@trains.route('/', methods=["get"])
@cross_origin()
def get_trains():
    return 'ok', 200
