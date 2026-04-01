import threading

from .app import app
from .socketio import *
from .routes import *
from .state import *
from .websocket import *

def run_server(host="0.0.0.0", port=5000):
    app.run(host=host, port=port, debug=False, use_reloader=False)

def start_server():
    t = threading.Thread(target=run_server, kwargs={
        "host": "0.0.0.0",
        "port": 5000,
    }, daemon=True)
    t.start()
