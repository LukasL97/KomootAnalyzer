from flask import Flask

from src.main.api.login import login_controller
from src.main.api.tours import tours_controller

app = Flask(__name__)


app.register_blueprint(login_controller)
app.register_blueprint(tours_controller)


@app.route('/')
def ping():
    return 'Hi, I am the KomootAnalyzer!'
