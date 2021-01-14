from ChessOpens.models import Opening, User
import random as rand
from sqlalchemy import or_


def check_valid_move(node, move, move_number, pgn):
    all_moves = get_all_possible(node, move_number, pgn)[0]
    return move in all_moves


def change_node(pgn,old_id, user_id=None):
    node = Opening.query.filter(Opening.pgn == pgn, or_(Opening.user_id == None, Opening.user_id==user_id))
    #node = Opening.query.filter(Opening.pgn.like("{}%".format(pgn)), or_(Opening.user_id == None, Opening.user_id==user_id))# Opening.user_id == user_id))
    if node.first() is None:
        return old_id
    return node.first().id
#    node = Opening.query.get(node_id)
#    #if move is contained in current node
#    if len(node.getMoves()) > move_number:
#        return node.id
#    #if move is contained in children
#    else:
#        if len(get_all_possible(node.id, move_number, pgn)[1]) == 1:
#            return get_all_possible(node.id, move_number, pgn)[1][0]
#        else:
#            return node.id
#

#returns string set as well as node list
def get_all_possible(node_id, move_number, pgn,user_id=None):
    node = Opening.query.get(node_id)
    node_list = []
    str_set = set()
    print("MOVE NUMBER")
    print(move_number)
    if len(node.getMoves()) > move_number:
        print(move_number)
        str_set.add(node.getMoves()[move_number-1])
        node_list.append(node.id)
    #if the node's pgn has been reached and it has children
    if node.hasChildren():
        for child in node.getChildren():
            if pgn in child.getPGN() and (child.user_id==user_id or child.user_id is None):
                #if the pgn is equal to the child's full pgn, return the child
                if pgn == child.getPGN():
                    sset, nlist = get_all_possible(child.id,move_number,pgn,user_id)
                    str_set = str_set | set(sset)
                    node_list += nlist
                    
                    
                    #if len(child.getMoves())>0:
                    #    str_set.add(child.getMoves()[-1]) 
                    #    node_list.append([child.id])

                #otherwise if
                elif move_number <= len(child.getMoves()):
                    str_set.add(child.getMoves()[move_number-1])
                    node_list.append(node.id)

            #if child.getPGN() in pgn and (child.user_id==user_id or child.user_id is None):
            #    sset, nlist = get_all_possible(child.id,move_number+1,pgn,user_id)
            #    str_set = str_set | set(sset)
            #    node_list += nlist
    #if the node has no children and its max pgn has been reached
    else:
       pass 

    return list(str_set), node_list
