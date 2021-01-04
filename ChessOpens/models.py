from ChessOpens import db


class Opening(db.Model):
   # __searchable__ = ["pgn", "name"]
    __tablename__ = 'opening'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('opening.id'))
    name = db.Column(db.String(512), unique=False,nullable=False)
    pgn = db.Column(db.String(1024), unique=True, nullable=False)
    children = db.relationship("Opening")

    def hasChildren(self):
        return len(self.children) > 0

    def addChild(self, pgn, name):
        opening = Opening(parent_id=self.id, name=name, pgn=pgn)
        db.session.add(opening)

    def getMoves(self):
        moves = self.pgn.split(" ")
        del moves[::3]
        return moves

    def getChildren(self):
        return self.children

    def getPGN(self):
        return self.pgn

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    favorites = db.Column(db.Integer)

    def __repr__(self):
        return f"User('{self.username}"

def addOpening(pgn, name, root=None):
    if root is None:
        root = Opening.query.first()
    #if there are no more nodes
    if not root.hasChildren():
        root.addChild(pgn, name)
    else:
        #check if a substring of pgn exists
        matching_op = None
        for opening in root.children:
            if opening.pgn in pgn:
                matching_op = opening
                break
        #if there are no children that match the pgn
        if matching_op is None:
            root.addChild(pgn, name)
        #if pgns are identical just exit and do nothing
        elif matching_op.pgn == pgn:
            pass
        #else recurse using the node that matches pgn
        else:
            addOpening(pgn, name, root=matching_op)
