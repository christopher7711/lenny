from itertools import product
from random import choice
from .game import evaluate
import asyncio

class Player():

    possible_evals = [k for k in product(range(5), repeat=2)
        if k[0] + k[1] < 5 and k != (1, 3)]

    def __init__(self, colors):
        self.checklist = list(product(colors, repeat=4))
        self.unused = self.checklist.copy()

    async def play(self, code=None):
        if code:
            self.unused.remove(code)
            return code
        optimal = (0, self.checklist[0])
        if len(self.checklist) in [1, len(self.unused)]:
            while True:
                code = choice(self.checklist)
                if len(set(code)) < 4 and len(self.checklist) == len(self.unused):
                    continue
                else:
                    break
            self.unused.remove(code)
            return code
        timeout = 0
        for code in [*self.checklist,
                *[el for el in self.unused if el not in self.checklist]]:
            timeout += 1
            min_removed = len(self.checklist)
            for evl in self.possible_evals:
                removed = 0
                for code_check in self.checklist:
                    w, k = evaluate(code, list(code_check))
                    if (w, k) != evl:
                        removed += 1                        
                if removed < min_removed:
                    min_removed = removed
                if removed == 0:
                    break
            if code in self.checklist:
                if min_removed >= optimal[0]:
                    optimal = (min_removed, code)
            else:
                if min_removed > optimal[0]:
                    optimal = (min_removed, code)
            if timeout * len(self.checklist) > 20 * len(self.unused):
                break
        self.unused.remove(optimal[1])
        return optimal[1]

    def elim(self, line):
        for code in self.checklist.copy():
            w, k = evaluate(code, line.pegs)
            if w != line.w or k != line.k:
                self.checklist.remove(code)
