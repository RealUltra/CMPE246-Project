from flask import redirect, send_from_directory

from .app import app, UI_DIR

@app.route("/")
def index():
    return send_from_directory(UI_DIR, "index.html")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(UI_DIR, "favicon.ico")

@app.route("/sketch.js")
def sketch():
    return send_from_directory(UI_DIR, "sketch.js")

@app.route("/socket-handler.js")
def socket_handler():
    return send_from_directory(UI_DIR, "socket-handler.js")

@app.route("/p5.min.js")
def p5():
    return send_from_directory(UI_DIR, "p5.min.js")

@app.route("/style.css")
def style():
    return send_from_directory(UI_DIR, "style.css")

@app.errorhandler(404)
def not_found(error):
    return redirect("/")
