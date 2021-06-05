from http.client import OK

import flask.globals
from flask import Blueprint, make_response, Response

from src.main.client.KomootClient import KomootClient

login_controller = Blueprint('login', __name__)


@login_controller.route('/login', methods=['POST'])
def login() -> Response:
    body = flask.globals.request.json
    client = KomootClient()
    user_id = client.login(body['email'], body['password'])
    response = make_response(user_id, OK)
    for key, value in client.get_cookies().items():
        response.set_cookie(key, value)
    response.set_cookie('komoot_user_id', user_id)
    return response
