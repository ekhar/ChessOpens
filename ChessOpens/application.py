from ChessOpens.models import Opening
import random as rand


def check_valid_move(node, move, move_number, pgn):
    all_moves = get_all_possible(node, move_number, pgn)[0]
    return move in all_moves


def change_node(node_id, move_number, pgn):
    node = Opening.query.get(node_id)
    #if move is contained in current node
    if len(node.getMoves()) > move_number:
        return node.id
    #if move is contained in children
    else:
        if len(get_all_possible(node.id, move_number, pgn)[1]) == 1:
            return get_all_possible(node.id, move_number, pgn)[1][0]
        else:
            return node.id


#returns string set as well as node list
def get_all_possible(node_id, move_number, pgn):
    node = Opening.query.get(node_id)
    node_list = []
    str_set = set()
    if len(node.getMoves()) > move_number:
        str_set.add(node.getMoves()[move_number])
        node_list.append(node.id)
    #if the node's pgn has been reached and it has children
    elif node.hasChildren():
        for child in node.getChildren():
            if pgn in child.getPGN():
                #if the pgn is equal to the child's full pgn, return the child
                if pgn == child.getPGN():
                    return child.getMoves()[-1], [child.id]

                #otherwise if
                elif move_number < len(child.getMoves()):
                    str_set.add(child.getMoves()[move_number])
                    node_list.append(node.id)
    #if the node has no children and its max pgn has been reached
    else:
       pass 

    return list(str_set), node_list
