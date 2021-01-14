from ChessOpens import db, login_manager
from flask_login import UserMixin

favorites = db.Table('favorites',
db.Column('user.id', db.Integer, db.ForeignKey('user.id')),
db.Column('opening.id', db.Integer, db.ForeignKey('opening.id'))
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#customs = db.Table('custom',
#db.Column('user.id', db.Integer, db.ForeignKey('user.id')),
#db.Column('opening.id', db.Integer, db.ForeignKey('opening.id'))
#)

class Opening(db.Model):
   # __searchable__ = ["pgn", "name"]
    __tablename__ = 'opening'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('opening.id'))
    name = db.Column(db.String(512), unique=False,nullable=False)
    pgn = db.Column(db.String(1024), unique=True, nullable=False)
    children = db.relationship("Opening")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def hasChildren(self):
        return len(self.children) > 0

    def addChild(self, pgn, name, user_id):
        opening = Opening(parent_id=self.id, name=name.strip(), pgn=pgn.strip(), user_id=user_id)
        self.children
        db.session.add(opening)
        db.session.commit()

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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    favorites = db.relationship("Opening", secondary=favorites, backref=db.backref("user_favorites"), lazy='dynamic')
    custom_op = db.relationship("Opening", backref=db.backref("user_custom", uselist='false'))



def addOpening(pgn, name, root=None, user_id=None):
    if root is None:
        root = Opening.query.first()
    #if there are no more nodes
    if not root.hasChildren():
        root.addChild(pgn, name, user_id)
    else:
        #check if a substring of pgn exists
        matching_op = None
        for opening in root.children:
            if opening.pgn in pgn:
                matching_op = opening
                break
        #if there are no children that match the pgn
        if matching_op is None:
            root.addChild(pgn, name, user_id)
        #if pgns are identical just exit and do nothing
        elif matching_op.pgn == pgn:
            pass
        #else recurse using the node that matches pgn
        else:
            addOpening(pgn, name, root=matching_op, user_id=user_id)
