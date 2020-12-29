from pgnReader import *
from pptree import *

origin = Opening("1.", "origin", [])

queensGambit1 = Opening("1. d4 d5", "queens gambit 1", [])
queensGambit2 = Opening("1. d4 d5 2. c4", "queens gambit 2", [])
queensGambit3 = Opening("1. d4 d5 2. b3", "queens gambit 3", [])

benoni1 = Opening("1. d4 Nf6", "benoni 1", [])
benoni2 = Opening("1. d4 Nf6 2. c4 c5 3. d5 e6", "benoni 2", [])

openings1 = [queensGambit1, queensGambit2, benoni1, benoni2, queensGambit3]
openings = [queensGambit1, queensGambit2, benoni2, benoni2]

openingTree = OpeningTree(origin)
openingTree1 = OpeningTree(origin)

for opening in openings1:
    openingTree.addOpening(opening)

print_tree(openingTree.root)