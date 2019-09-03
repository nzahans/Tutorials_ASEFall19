import re, sys
from Num import Num


class THE:
    sep = ","
    num = "$"
    less = "<"
    more = ">"
    skip = "?"
    doomed = r'([\n\t\r ]|#.*)'


class Tbl:
    global globalOid
    listOfRead = []  # processed output from read
    listOfRow = []  # list of row objects
    listOfCol = []  # list of col object

    def __init__(self):
        self.globalOid = 1  # oid implementation need improvement

    def incrOid(self):
        self.globalOid += 1
        return self.globalOid;

    def read(self, file):
        firstRow = []
        for cell in cells(cols(rows(string(file)))):
            print(cell)
            self.listOfRead.append(cell)  # store all processed output
            # print("cells:", cell, type(cell))

            if firstRow == []:  # check init title list is empty
                firstRow = cell
                # print("text:", firstRow, type(firstRow))
                for i, t in enumerate(firstRow):
                    col = Col(0, i, t)
                    self.listOfCol.append(col)
            else:
                row = Row(0, cell, [], 0)
                self.listOfRow.append(row)  # each row is a Row object
                # print("cell0", cell[0])

    def dump(self):

        # print("listOfRead:", self.listOfRead)

        # for i in self.listOfRow:
        #     print("each row object:", i.cells)

        numInstance = [None] * len(self.listOfCol)
        # print(numInstance)
        for i in range(len(self.listOfCol)):
            # print(i)
            numInstance[i] = Num()
        # print(numInstance)

        for _, item in enumerate(self.listOfRead[1:len(self.listOfRead)]):
            # print("item:", item, type(item))
            for j in self.listOfCol:
                # print("pos:", j.pos, "num:", item[j.pos])
                if (item[j.pos] == THE.skip):
                    numInstance[j.pos].__add__(0)  # use 0 for ? in hw2
                else:
                    numInstance[j.pos].__add__(item[j.pos])

        # print(numInstance)

        # for i in range(len(self.listOfCol)):
        #     print(numInstance[i].expect())

        print("")
        print("t.cols")

        for i in range(len(self.listOfCol)):
            print("| ", i + 1)
            print("| | add:", "Num1")
            print("| | col:", i + 1)
            print("| | hi:", numInstance[i].hi)
            print("| | lo:", numInstance[i].lo)
            print("| | m2:", "{:.3f}".format(numInstance[i].m2))
            print("| | mu:", "{:.3f}".format(numInstance[i].expect()))
            print("| | n:", len(self.listOfRead))
            print("| | oid:", self.incrOid())
            print("| | sd:", "{:.3f}".format(numInstance[i].delta()))
            print("| | txt:", self.listOfCol[i].txt)

        print("t.oid:", self.globalOid)

        print("t.rows:", )
        for i, element in enumerate(self.listOfRow):
            print("| ", i + 1)
            print("| | cells")
            for j in range(len(element.cells)):
                print("| | | ", j + 1, ":", element.cells[j])
            print("| | ", "cooked")  # Need further implementation
            print("| | dom:", 0)
            print("| | oid:", self.incrOid())


class Col:
    def __init__(self, oid=0, pos=0, txt=None):
        self.oid = oid
        self.pos = pos
        self.txt = txt


class Row:
    def __init__(self, oid, cells=[], cooked=[], dom=0):
        self.oid = oid
        self.cells = cells
        self.cooked = cooked
        self.dom = dom


def string(s):
    """read lines from a string"""
    for line in s.splitlines():
        yield line


def rows(src):
    """convert lines into lists, killing whitespace
    and comments. skip over lines of the wrong size"""
    linesize = None
    for n, line in enumerate(src):
        line = re.sub(THE.doomed, '', line.strip())
        if line:
            line = line.split(THE.sep)  # breakup a string and add the data to a string array
            if linesize is None:
                linesize = len(line)
            if len(line) == linesize:
                yield line
            else:
                print("E> skipping line %s" % n, file=sys.stderr)  # To print to STDERR


def cols(src):
    """skip columns whose name contains '?'"""
    usedCol = None
    for cells in src:
        # usedCol = usedCol or [n for n, cell in enumerate(cells) if not THE.skip in cell]
        if usedCol is None:
            usedCol = [n for n, cell in enumerate(cells) if not THE.skip in cell]
        yield [cells[n] for n in usedCol]


def cells(src):
    """convert strings into their right types"""
    one = next(src)
    fs = [None] * len(one)  # [None, None, None, None]
    yield one  # the first line

    def ready(n, cell):
        if cell == THE.skip:
            return cell  # skip over '?'
        fs[n] = fs[n] or prep(one[n])  # ensure column 'n' compiles
        return fs[n](cell)  # compile column 'n'

    for _, cells in enumerate(src):
        # print("cells:", cells)
        yield [ready(n, cell) for n, cell in enumerate(cells)]


def prep(x):
    """return something that can compile strings"""

    def num(z):
        f = float(z)
        i = int(f)
        return i if i == f else f

    # --------------------------------------------------------
    for c in [THE.num, THE.less, THE.more]:
        if c in x:
            return num


def main():
    file = """
    $cloudCover, $temp, ?$humid, <wind,  $playHours
    100,        68,    80,    0,    3   # comments
    0,          85,    85,    0,    0
    
    0,          80,    90,    10,   0
    60,         83,    86,    0,    4
    100,        70,    96,    0,    3
    100,        65,    70,    20,   0
    70,         64,    65,    15,   5
    0,          72,    95,    0,    0
    0,          69,    70,    0,    4
    ?,          75,    80,    0,    ?
    0,          75,    70,    18,   4
    60,         72,
    40,         81,    75,    0,    2
    100,        71,    91,    15,   0
    """

    tbl = Tbl()
    tbl.read(file)
    tbl.dump()


if __name__ == "__main__":
    main()
