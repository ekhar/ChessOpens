import chess
from pgnReader import OpeningTree, Opening
import random as rand
from pptree import *

player_white = True

#setting up Tree
#remodel later
origin = Opening("1.", "origin", [])

queensGambit1 = Opening("1. d4 d5", "queens gambit 1", [])
queensGambit2 = Opening("1. d4 d5 2. c4", "queens gambit 2", [])
queensGambit3 = Opening("1. d4 d5 2. b3", "queens gambit 3", [])

benoni1 = Opening("1. d4 Nf6", "benoni 1", [])
benoni2 = Opening("1. d4 Nf6 2. c4 c5 3. d5 e6", "benoni 2", [])

kings = Opening("1. e4 e5", "kings", [])

openings = [
    queensGambit1, queensGambit2, benoni1, benoni2, queensGambit3, kings
]

openingTree = OpeningTree(origin)

for opening in openings:
    openingTree.addOpening(opening)
#End of this

board = chess.Board()

current_node = openingTree.root

print_tree(openingTree.root)


def check_valid_move(node, move, move_number, pgn):
    all_moves = get_all_possible(node, move_number, pgn)[0]
    return move in all_moves


def change_node(node, move, move_number, valid, pgn):
    #if the move is valid
    if valid:
        #if move is contained in current node
        if len(node.getMoves()) > move_number:
            return node
        #if move is contained in children
        else:
            if len(get_all_possible(node, move_number, pgn)[1]) == 1:
                return get_all_possible(node, move_number, pgn)[1][0]
            else:
                return node

    #return current node for invalid moves
    else:
        return node


#returns string set as well as node list
def get_all_possible(node, move_number, pgn):
    node_list = []
    str_set = set()
    if len(node.getMoves()) > move_number:
        str_set.add(node.getMoves()[move_number])
        node_list.append(node)
    #if the node's pgn has been reached and it has children
    elif node.hasChildren():
        for child in node.getChildren():
            if pgn in child.getPGN():
                #if the pgn is equal to the child's full pgn, return the child
                if pgn == child.getPGN():
                    return set(child.getMoves()[-1]), [child]

                #otherwise if
                elif move_number < len(child.getMoves()):
                    str_set.add(child.getMoves()[move_number])
                    node_list.append(node)
    #if the node has no children and its max pgn has been reached
    else:
        pass

    return str_set, node_list


def printPGN(pgn, move_num):
    if move_num == 0:
        print("")

    elif pgn[-1] == ".":
        pgn_print = pgn.split(" ")
        pgn_print.pop()
        print(" ".join(pgn_print))

    else:
        print("")
        print(pgn)


move_num = 0
pgn = ""

while True:
    pgn_copy = pgn
    #creates copy for invalid moves
    if move_num == 0:
        pgn = "1."

    print("\n")
    print(board)

    printPGN(pgn, move_num)

    #white's turn
    if move_num % 2 == 0 and player_white:
        move = input("Where to move? ")

        if move == "exit":
            break
        #if this is not a legal move checker
        try:
            board.push_san(move)
            board.pop()
        except:
            print("White legally cannot make this move. Please type again")
            print("Legal moves include in our database include " +
                  str(get_all_possible(current_node, move_num, pgn)[0]))
            pgn = pgn_copy
            continue

        #update pgn, determine validity and the current node
        pgn += " " + move
        valid = check_valid_move(current_node, move, move_num, pgn)
        current_node = change_node(current_node, move, move_num, valid, pgn)

    #black's turn
    elif move_num % 2 == 1 and not player_white:
        move = input("Where to move? ")
        if move == "exit":
            break

        #if the move is legal checker
        try:
            board.push_san(move)
            board.pop()
        except:
            print("Black cannot legally make this move. Please type again")
            print("Legal moves in our database include " +
                  get_all_possible(current_node, move_num, pgn)[0])
            pgn = pgn_copy
            continue

        #update pgn
        pgn += " " + move
        valid = check_valid_move(current_node, move, move_num, pgn)
        current_node = change_node(current_node, move, move_num, valid, pgn)

    #computer's turn gets all possible moves and randomly selects one
    else:
        valid = True
        all_moves = list(get_all_possible(current_node, move_num, pgn)[0])
        move = rand.choice(all_moves)
        pgn += " " + move
        current_node = change_node(current_node, move, move_num, valid, pgn)
        print("\nComputer moves " + move)

    #if move was not valid, redo without adding to while
    if not valid:
        print("Not a valid move/ not within our database. Please try again")
        print("Moves within our database includes: " +
              str(get_all_possible(current_node, move_num, pgn)[0]))
        #reset pgn
        pgn = pgn_copy
        continue

    #if move was valid, check to see if it was the end of the line
    else:
        move_num += 1
        board.push_san(move)
        #update pgn's number
        if move_num % 2 == 0 and move_num != 1:
            pgn += " " + str(1 + (move_num // 2)) + "."
        #check to see if it is the end of the line
        if len(current_node.getMoves()
               ) <= move_num and not current_node.hasChildren():
            print("\n")
            print(board)
            print("This is the end of the current line")
            break

exit()