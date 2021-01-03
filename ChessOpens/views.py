from flask import render_template, url_for, jsonify, session, request
from flask_session import Session
from ChessOpens import app, db
from ChessOpens.models import Opening
from ChessOpens.application import change_node, get_all_possible
import re

@app.route('/', methods=["GET", "POST"])
def home():
    #set node_id up with origin's id
    id = 1
    move_number = 0
    pgn = Opening.query.first().pgn
    # all possible moves
    db_moves = get_all_possible(id, move_number, pgn)[0]
    #current node name
    op_name = Opening.query.get(id).name
    openings = Opening.query.all()
    return render_template("home.html",
                           op_data={
                               "op_name": op_name,
                               "db_moves": list(db_moves),
                               "id": id,
                           },
                           openings=openings)


@app.route('/update', methods=["GET", "POST"])
def update_nodes():
    if request.method == "POST":
        #pull info from js query
        pgn = request.get_json()["pgn"]
        id = request.get_json()["id"]
        moves = pgn.split(" ")
        #find the last period in pgn bc move numbers always before period in pgn
        if (len(pgn) == 0):
            move_number = 0
        #black just moved
        elif len(pgn.split(" ")) % 3 <= 1:
            #regex to find third to last number
            move_number = 2 * int(re.findall(r'\d+', pgn)[-3])
        #white just moved
        else:
            #regex to find second to last number
            move_number = 2 *int(re.findall(r'\d+', pgn)[-2])- 1
        
        print(move_number)

        #gets node_id to properly update
        id = change_node(id, move_number, pgn)
        node = Opening.query.get(id)
        db_moves = get_all_possible(id, move_number, pgn)[0]
        return jsonify({
            "op_name": node.name,
            "db_moves": list(db_moves),
            "id": id
        })
