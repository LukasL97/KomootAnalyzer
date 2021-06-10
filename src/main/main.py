from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS

from src.main.api.login import login_controller
from src.main.api.tours import tours_controller

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['wsgi']
        },
        'pykka': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    }
})

app = Flask(__name__)

CORS(
    app,
    supports_credentials=True,
    origins=['http://localhost:3000']
)

app.register_blueprint(login_controller)
app.register_blueprint(tours_controller)


@app.route('/')
def ping():
    return 'Hi, I am the KomootAnalyzer!'
