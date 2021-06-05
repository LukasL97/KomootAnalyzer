from logging.config import dictConfig

from flask import Flask

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
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

app.register_blueprint(login_controller)
app.register_blueprint(tours_controller)


@app.route('/')
def ping():
    return 'Hi, I am the KomootAnalyzer!'
