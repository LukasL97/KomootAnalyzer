from http.client import OK

import flask.globals
from flask import Blueprint, Response, make_response, jsonify

from src.main.dao.ToursDAO import ToursDAO
from src.main.serialization.TourSerializer import TourSerializer
from src.main.worker.ToursUpdateWorker import ToursUpdateWorker, ToursUpdateMessage

tours_controller = Blueprint('tours', __name__)


@tours_controller.route('/tours', methods=['PATCH'])
def update_tours() -> Response:
    cookies = dict(flask.globals.request.cookies)
    assert 'komoot_user_id' in cookies.keys()
    worker = ToursUpdateWorker.start()
    worker.tell(ToursUpdateMessage(cookies))
    return make_response('OK', OK)


@tours_controller.route('/tours', methods=['GET'])
def get_tours() -> Response:
    cookies = dict(flask.globals.request.cookies)
    assert 'komoot_user_id' in cookies.keys()
    tours = ToursDAO.find_by_user(cookies['komoot_user_id'])
    tours = [TourSerializer.serialize(tour) for tour in tours]
    return make_response(jsonify(tours), OK)
