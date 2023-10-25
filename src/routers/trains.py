from flask import Blueprint

from services.trains_service import TrainsService


trains = Blueprint('trains', __name__)

trains_service = TrainsService()
