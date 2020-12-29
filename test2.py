class Node:
    def __init__(self, name, children=[]):
        self.name = name
        self.children = children

    def addchild(self, op):
        self.children.append(op)

    def printChildren(self):
        print([str(child) for child in self.children])

    def __str__(self):
        return self.name


class Tree:
    def __init__(self, root):
        self.root = root

    def add(self, op):
        self.root.addchild(op)

    def pprint_tree(self, root=None, level=0, ret=""):
        if root is None:
            root = self.root

        ret = ret + str("--" * level + root.name + "\n")
        for child in root.children:
            return self.pprint_tree(child, level + 1, ret)
        if len(root.children) == 0:
            print(ret)


five = Node("five")
four = Node("four")
three = Node("three")
two = Node("two")
one = Node("one", [])

tree = Tree(one)

#tree.add(two)
one.printChildren()
tree.add(three)
#tree.pprint_tree()

from pptree import *

print_tree(one)