import random


class Num():
    "Track numbers seen in a column"

    def __init__(self, inits=[]):
        self.n, self.mu, self.m2 = 0, 0, 0
        self.lo, self.hi = 10 ** 32, -1 * 10 ** 32
        [self + x for x in inits]

    def delta(self):
        return self.sd()

    def expect(self):
        return self.mu

    def sd(self):
        return 0 if self.n < 2 else (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5

    def __add__(self, x):
        if x < self.lo:
            self.lo = x
        if x > self.hi:
            self.hi = x

        self.n += 1
        d = x - self.mu
        self.mu += d / self.n
        self.m2 += d * (x - self.mu)

    def __sub__(self, x):
        if self.n < 2:
            self.n, self.mu, self.m2 = 0, 0, 0
        else:
            self.n -= 1
            d = x - self.mu
            self.mu -= d / self.n
            self.m2 -= d * (x - self.mu)


def main():
    print("Generate list with 100 random numbers between 1 and 200")
    test_randoms = random.sample(range(200), 100)
    print(test_randoms)
    print("")

    numAddInstance = Num()
    meanAddList = []
    sdAddList = []
    index = 1
    for randomNum in test_randoms:
        numAddInstance + randomNum
        if index % 10 == 0:
            meanAddList.append(round(numAddInstance.expect(), 2)), sdAddList.append(round(numAddInstance.delta(), 2))
        index += 1

    numSubInstance = Num(test_randoms)
    meanSubList = []
    sdSubList = []
    index = 100
    for randomNum in reversed(test_randoms):
        if index % 10 == 0:
            meanSubList.append(round(numSubInstance.expect(), 2)), sdSubList.append(round(numSubInstance.delta(), 2))
        numSubInstance - randomNum
        index -= 1

    meanSubList.reverse()
    sdSubList.reverse()
    print("mean Add list: ", meanAddList)
    print("mean sub List: ", meanSubList)
    print("sd Add List: ", sdAddList)
    print("sd sub List: ", sdSubList)


if __name__ == "__main__":
    main()
