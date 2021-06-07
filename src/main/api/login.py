from http.client import OK, BAD_REQUEST, UNAUTHORIZED

import flask.globals
from flask import Blueprint, make_response, Response

from src.main.client.KomootClient import KomootClient
from src.main.client.exception import KomootAuthorizationException

login_controller = Blueprint('login', __name__)


@login_controller.route('/login', methods=['POST'])
def login() -> Response:
    body = flask.globals.request.json
    client = KomootClient()
    try:
        user_id = client.login(body['email'], body['password'])
    except KeyError:
        return make_response('Body needs to contain "email" and "password"', BAD_REQUEST)
    except KomootAuthorizationException:
        return make_response(f'Authorization failed for email {body["email"]}', UNAUTHORIZED)
    response = make_response(user_id, OK)
    for key, value in client.get_cookies().items():
        response.set_cookie(key, value)
    response.set_cookie('komoot_user_id', user_id)
    return response
