from collections import defaultdict
import math


class Sym:

    def f(x):
        return x

    def __init__(self, pairs=[], f=f):
        self.counts = defaultdict(int)
        self.mode = None
        self.most = 0
        self.n = 0
        self._ent = None
        for x in pairs:
            self.symInc(f(x))

    def symInc(self, x):
        if x == "?":
            return x
        self._ent = None
        self.n += 1
        self.counts[x] += 1
        if self.counts[x] > self.most:
            self.most = self.counts[x]
            self.mode = x
        return x

    def symDec(self, x):
        self._ent = None
        if self.n > 0:
            self.n -= 1
        self.counts[x] -= 1
        return x

    def symEnt(self):
        if self._ent is None:
            self._ent = 0
            for x, n in self.counts.items():
                p = n / self.n
                self._ent -= p * math.log(p, 2)
        return self._ent


def main():
    testlist = ['a', 'a', 'a', 'a', 'b', 'b', 'c']
    sym = Sym(testlist)
    print(sym.symEnt())


if __name__ == "__main__":
    main()
