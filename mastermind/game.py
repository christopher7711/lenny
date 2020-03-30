from random import choice

class Board():

    def __init__(self, colors=None, solution=None, size=10):
        self.lines = [Line() for i in range(size)]
        if colors:
            self.solution = [choice(colors) for i in range(4)]
        else:
            self.solution = solution

class Line():

    def __init__(self):
        self.pegs = [None] * 4

    def fill(self, code):
        self.pegs = list(code)

    def eval(self, sol):
        self.w, self.k = evaluate(self.pegs, sol)
    
    def assist(self, w, k):
        self.w = int(w)
        self.k = int(k)

def evaluate(code1, code2):
    _code2 = code2.copy()
    w, k = 0, 0
    for a, b in zip(code1, code2):
        if a == b:
            k += 1
        if a in _code2:
            w += 1
            _code2.remove(a)
    return w - k, k
