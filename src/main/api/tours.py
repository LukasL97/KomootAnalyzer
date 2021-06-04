from http.client import OK

from flask import Blueprint, Response, make_response

from src.main.worker.ToursUpdateWorker import ToursUpdateWorker, ToursUpdateMessage

tours_controller = Blueprint('tours', __name__)


@tours_controller.route('/tours', methods=['PATCH'])
def update_tours() -> Response:
    worker = ToursUpdateWorker.start()
    worker.tell(ToursUpdateMessage())
    return make_response('OK', OK)
