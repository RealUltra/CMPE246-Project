import os

from flask import Flask
from flask_sock import Sock

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")

app = Flask(__name__, static_folder=UI_DIR, static_url_path="")
sock = Sock(app)