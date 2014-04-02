from flask import Flask
from flask.ext.assets import Environment

app = Flask(__name__)
assets = Environment(app)

app.config.from_object('config')

from app import views

