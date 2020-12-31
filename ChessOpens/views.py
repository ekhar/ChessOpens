from flask import render_template, url_for
from ChessOpens import app


@app.route('/')
def hello_world():
    return render_template("home.html")
