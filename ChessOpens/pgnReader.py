import chess


class Opening:
    def __init__(self, pgn, name, children=[], fen=''):
        self.pgn = pgn

        self.moves = pgn.split(" ")
        del self.moves[::3]

        self.name = name
        self.children = children
        self.fen = fen
        if (self.fen == ''):
            board = chess.Board()
            for move in self.moves:
                board.push(move)
            self.fen = board.fen()

    def hasChildren(self):
        return len(self.children) > 0

    def addChild(self, opening):
        self.children.append(opening)

    def getMoves(self):
        return self.moves

    def getChildren(self):
        return self.children

    def getPGN(self):
        return self.pgn

    def __str__(self):
        return self.name


class OpeningTree:
    def __init__(self, root):
        self.root = root

    def getRoot(self):
        return self.root

    def addOpening(self, op, root=None):
        if root is None:
            root = self.root

        #if there are no more nodes
        if not root.hasChildren():
            root.addChild(op)

        else:
            #check if a substring of pgn exists
            matching_op = None
            for opening in root.children:
                if opening.pgn in op.pgn:
                    matching_op = opening
                    break

            #if there are no children that match the pgn
            if matching_op is None:
                root.addChild(op)
            elif matching_op.pgn == op.pgn:
                pass
            #else recurse using the node that matches pgn
            else:
                self.addOpening(op, root=matching_op)
