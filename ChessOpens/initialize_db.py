from ChessOpens import db

from ChessOpens.models import Opening,addOpening 

try: 
    Opening.query.first()
except:
    db.create_all()

    start = Opening(parent_id=0,name="Starting Board", pgn="1.")
    if (Opening.query.get(1) is None):
        db.session.add(start)
        db.session.commit()


    import json

    #addOpening(name="queens gambit declined", pgn="1. d4 d5 2. c4 e3")
    #addOpening(name="Kings Pawn", pgn="1. e4")
    #addOpening(name="Sicilian", pgn="1. e4 c5")
    #addOpening(name="English", pgn="1. c4")
    #db.session.commit()

    with open('./ChessOpens/codes.json') as f:
        openings = json.load(f)

    d = {}
    for key in openings.keys():
        name = openings[key]["name"]
        pgn = openings[key]["moves"]
        d[pgn] = name

    for key in d.keys():
        name = d[key]
        addOpening(name=name,pgn=key)
        db.session.commit()

