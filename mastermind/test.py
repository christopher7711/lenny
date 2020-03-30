from game import *
from player import *

colors = 'qwerty'
lst = []

for i in range(100):
    board = Board(colors=colors)
    player = Player(colors)
    board.lines[0].fill(player.play(code=tuple('qwqw')))
    board.lines[0].eval(board.solution)
    player.elim(board.lines[0])
    lst.append(len(player.checklist))
    print(len(player.checklist))
print(sum(lst)/len(lst))
