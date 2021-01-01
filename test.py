from ChessOpens import db
from ChessOpens.models import Opening, addOpening

#db.create_all()
#origin = Opening(pgn="1.", name="origin")
#db.session.add(origin)

addOpening(name="queens gambit declined", pgn="1. d4 d5 2. c4 e3")
addOpening(name="Kings Pawn", pgn="1. e4")
addOpening(name="Sicilian", pgn="1. e4 c5")
addOpening(name="English", pgn="1. c4")

db.session.commit()

print(Opening.query.all())
print(Opening.query.first().children[0].getMoves())