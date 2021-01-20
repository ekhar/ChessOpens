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

#levels to the tree could be descrbed a len(opening.moves)
def order_tree(level=0,node=None):
    if node is None:
        node = Opening.query.get(1)
    queue = []
    visited=[]
    visited.append(node)
    queue.append(node)
    count = 0
    while queue:
        count+=1
        s = queue.pop(0) 
        
        #addOpening(s.name,s.pgn,premade_op=s)
        
        for child in s.children:
            if child not in visited:
                visited.append(child)
                queue.append(child)


    #order_tree(level=level,root=child)

def bfs(node):
    queue = []
    visited=[]
    visited.append(node)
    queue.append(node)
    count = 0
    while queue:
        count+=1
        s = queue.pop(0) 
        print (s, end = " ") 
        
        for child in s.children:
            if child not in visited:
                visited.append(child)
                queue.append(child)
    print(count)

#if opening does not match its level then breadth wide search to see if another opening's pgn is a substring of it
    #if this is true
        # recursivley delete opening and children
        # re-add opening to the tree 
        # restart this whole method
        #------or-------
        #Change openings parent id to where it should be added
    #if this is not true
        #keep checking this until level len(node.moves) == len(opening.moves)
        #then pass