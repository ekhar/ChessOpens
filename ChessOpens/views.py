from flask import render_template, url_for, jsonify, session, request
from flask_session import Session
from ChessOpens import app, db
from ChessOpens.models import Opening
from ChessOpens.application import change_node, get_all_possible


@app.route('/', methods=["GET", "POST"])
def random_moves():
    #set node_id up with origin's id
    id = 1
    move_number = 0
    pgn = Opening.query.first().pgn
    # all possible moves
    db_moves = get_all_possible(id, move_number, pgn)[0]
    #current node name
    op_name = Opening.query.get(session["node_id"]).name
    return render_template("home.html",
                           op_data={
                               "op_name": op_name,
                               "db_moves": list(db_moves),
                               "id": session["node_id"]
                           })


@app.route('/update', methods=["GET", "POST"])
def update_nodes():
    if request.method == "POST":
        #pull info from js query
        pgn = request.get_json()["pgn"]
        id = request.get_json()["id"]
        print(id)
        #find the last period in pgn bc move numbers always before period in pgn
        if (len(pgn) == 0):
            move_number = 0
        elif len(pgn.split(" ")) % 3 <= 1:
            move_number = 2 * int(pgn[pgn.rfind(".") - 1])
        else:
            move_number = 2 * int(pgn[pgn.rfind(".") - 1]) - 1

        #gets node_id to properly update
        id = change_node(id, move_number, pgn)
        node = Opening.query.get(id)
        db_moves = get_all_possible(id, move_number, pgn)[0]
        print(id)
        print(db_moves)
        print(node.name)
        return jsonify({
            "op_name": node.name,
            "db_moves": list(db_moves),
            "id": id
        })
