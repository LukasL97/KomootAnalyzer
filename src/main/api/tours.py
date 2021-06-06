from http.client import OK, CONFLICT

import flask.globals
from flask import Blueprint, Response, make_response, jsonify
from pykka import ActorRegistry

from src.main.dao.ToursDAO import ToursDAO
from src.main.serialization.TourSerializer import TourSerializer
from src.main.worker.ToursUpdateWorker import ToursUpdateWorker, ToursUpdateMessage

tours_controller = Blueprint('tours', __name__)


@tours_controller.route('/tours/sync', methods=['PATCH'])
def update_tours() -> Response:
    cookies = dict(flask.globals.request.cookies)
    assert 'komoot_user_id' in cookies.keys()
    user_id = cookies['komoot_user_id']
    if user_id in [w._actor.user_id for w in ActorRegistry.get_by_class(ToursUpdateWorker)]:
        return make_response(f'Tours update is already running for user with id {user_id}', CONFLICT)
    else:
        worker = ToursUpdateWorker.start(user_id)
        worker.tell(ToursUpdateMessage(cookies))
        return make_response(f'Started updating tours from recorded komoot tours for user with id {user_id}', OK)


@tours_controller.route('/tours', methods=['GET'])
def get_tours() -> Response:
    cookies = dict(flask.globals.request.cookies)
    assert 'komoot_user_id' in cookies.keys()
    tours = ToursDAO.find_by_user(cookies['komoot_user_id'])
    tours = [TourSerializer.serialize(tour) for tour in tours]
    return make_response(jsonify(tours), OK)
