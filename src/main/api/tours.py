from http.client import OK

import flask.globals
from flask import Blueprint, Response, make_response

from src.main.worker.ToursUpdateWorker import ToursUpdateWorker, ToursUpdateMessage

tours_controller = Blueprint('tours', __name__)


@tours_controller.route('/tours', methods=['PATCH'])
def update_tours() -> Response:
    cookies = dict(flask.globals.request.cookies)
    assert 'komoot_user_id' in cookies.keys()
    worker = ToursUpdateWorker.start()
    worker.tell(ToursUpdateMessage(cookies))
    return make_response('OK', OK)
