from flask import render_template, url_for, jsonify, session, request
from flask_session import Session
from ChessOpens import app, db
from ChessOpens.models import Opening
from ChessOpens.application import *


@app.route('/', methods=["GET", "POST"])
def random_moves():
    if request.method == "POST":
        move = request.get_json()["move"]
        pgn = request.get_json()["pgn"]
        #find the last period in pgn bc move numbers always before period in pgn
        if move["color"] == 'b':
            move_number = 2 * int(pgn[pgn.rfind(".") - 1])
        else:
            move_number = 2 * int(pgn[pgn.rfind(".") - 1]) - 1

        session["node_id"] = change_node(session["node_id"], move["san"],
                                         move_number, pgn)

        db_moves = get_all_possible(session["node_id"], move_number, pgn)[0]
        op_name = Opening.query.get(session["node_id"]).name

    #page first loads up
    else:
        session["node_id"] = Opening.query.first().id
    return render_template("home.html")