class Abcd(object):
    def __init__(self):
        self.known = []  # save all classes
        self.yes = 0
        self.no = 0
        self.rx = 'rx'
        self.data = 'data'
        self.a = {}
        self.b = {}
        self.c = {}
        self.d = {}

    def Abcd1(self, want, got):
        if want not in self.known:
            self.known.append(want)
            self.a[want] = self.yes + self.no
            self.b[want] = 0
            self.c[want] = 0
            self.d[want] = 0
        if got not in self.known:
            self.known.append(got)
            self.a[got] = self.yes + self.no
            self.b[got] = 0
            self.c[got] = 0
            self.d[got] = 0

        if want == got:
            self.yes += 1
        else:
            self.no += 1

        for x in self.known:
            if want == x:
                if want == got:
                    self.d[x] += 1
                else:
                    self.b[x] += 1
            else:
                if got == x:
                    self.c[x] += 1
                else:
                    self.a[x] += 1

    def AbcdReport(self):
        s = " |"
        ds = "-----"

        # Center align values
        print('{:^5}'.format('db'), s, '{:^5}'.format('rx'), s, '{:^5}'.format('num'), s, '{:^5}'.format('a'), s,
              '{:^5}'.format('b'), s,
              '{:^5}'.format('c'), s, '{:^5}'.format('d'), s, '{:^5}'.format('acc'), s, '{:^5}'.format('pre'), s,
              '{:^5}'.format('pd'), s,
              '{:^5}'.format('pf'), s, '{:^5}'.format('f'), s, '{:^5}'.format('g'), s, '{:^5}'.format('class'))
        print('{:^5}'.format(ds), s, '{:^5}'.format(ds), s, '{:^5}'.format(ds), s, '{:^5}'.format(ds), s,
              '{:^5}'.format(ds), s,
              '{:^5}'.format(ds), s, '{:^5}'.format(ds), s, '{:^5}'.format(ds), s, '{:^5}'.format(ds), s,
              '{:^5}'.format(ds), s,
              '{:^5}'.format(ds), s, '{:^5}'.format(ds), s, '{:^5}'.format(ds), s, '{:^5}'.format(ds))

        for x in self.known:
            pd = pf = pn = prec = g = f = acc = 0
            a = self.a[x]
            b = self.b[x]
            c = self.c[x]
            d = self.d[x]

            if b + d > 0:
                pd = d / (b + d)

            if a + c > 0:
                pf = c / (a + c)

            if a + c > 0:
                pn = (b + d) / (a + c)

            if c + d > 0:
                prec = d / (c + d)

            if 1 - pf + pd > 0:
                g = 2 * (1 - pf) * pd / (1 - pf + pd)

            if prec + pd > 0:
                f = 2 * prec * pd / (prec + pd)

            if self.yes + self.no > 0:
                acc = self.yes / (self.yes + self.no)

            print('{:^5}'.format(self.data), s, '{:^5}'.format(self.rx), s, '{:^5}'.format(self.yes + self.no), s,
                  '{:^5}'.format(a), s,
                  '{:^5}'.format(b), s,
                  '{:^5}'.format(c), s, '{:^5}'.format(d), s, '{:5.2f}'.format(acc), s, '{:5.2f}'.format(prec), s,
                  '{:5.2f}'.format(pd), s,
                  '{:5.2f}'.format(pf), s, '{:5.2f}'.format(f), s, '{:5.2f}'.format(g), s, '{:^5}'.format(x))


def main():
    abcd = Abcd()

    for j in range(0, 6):
        abcd.Abcd1("yes", "yes")

    for j in range(0, 2):
        abcd.Abcd1("no", "no")

    for j in range(0, 5):
        abcd.Abcd1("maybe", "maybe")

    abcd.Abcd1("maybe", "no")
    abcd.AbcdReport()

    #  db    |  rx    |  num   |   a    |   b    |   c    |   d    |  acc   |  pre   |  pd    |  pf    |   f    |   g    | class
    # -----  | -----  | -----  | -----  | -----  | -----  | -----  | -----  | -----  | -----  | -----  | -----  | -----  | -----
    # data   |  rx    |  14    |   8    |   0    |   0    |   6    |  0.93  |  1.00  |  1.00  |  0.00  |  1.00  |  1.00  |  yes
    # data   |  rx    |  14    |  11    |   0    |   1    |   2    |  0.93  |  0.67  |  1.00  |  0.08  |  0.80  |  0.96  |  no
    # data   |  rx    |  14    |   8    |   1    |   0    |   5    |  0.93  |  1.00  |  0.83  |  0.00  |  0.91  |  0.91  | maybe


if __name__ == "__main__":
    main()
