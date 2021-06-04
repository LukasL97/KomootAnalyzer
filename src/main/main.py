from flask import Flask

from src.main.api.login import login_controller

app = Flask(__name__)


app.register_blueprint(login_controller)


@app.route('/')
def ping():
    return 'Hi, I am the KomootAnalyzer!'
