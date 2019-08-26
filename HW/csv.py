# /* vim: set ts=2 sts=2 sw=2 et : */
# --------- --------- --------- --------- --------- ---------
# https://gist.github.com/timm/08a7e6a7188b227ec3f294f354dfbecc

import re, sys, zipfile


class THE:
    sep = ","
    num = "$"
    less = "<"
    more = ">"
    skip = "?"
    doomed = r'([\n\t\r ]|#.*)'


def prep(x):
    "return something that can compile strings"

    def num(z):
        f = float(z)
        i = int(f)
        return i if i == f else f

    # --------------------------------------------------------
    for c in [THE.num, THE.less, THE.more]:
        if c in x:
            return num
    return str


def string(s):
    "read lines from a string"
    for line in s.splitlines(): yield line


def file(fname):
    "read lines from a fie"
    with open(fname) as fs:
        for line in fs: yield line


def zipped(archive, fname):
    "read lines from a zipped file"
    with zipfile.ZipFile(archive) as z:
        with z.open(fname) as f:
            for line in f: yield line


def rows(src):
    """convert lines into lists, killing whitespace
    and comments. dodging lines of the wrong size"""
    want = None
    for n, line in enumerate(src):
        line = re.sub(THE.doomed, '', line.strip())
        if line:
            line = line.split(THE.sep)
            if want is None: want = len(line)
            if len(line) == want:
                yield line
            else:
                print("E> skipping line %s" % n, file=sys.stderr)


def cols(src):
    "skip columns whose name contains '?'"
    use = None
    for cells in src:
        use = use or [n for n, cell in enumerate(cells)
                      if not THE.skip in cell]
        yield [cells[n] for n in use]


def cells(src):
    "convert strings into their right types"

    def ready(n, cell):
        if cell == THE.skip: return cell  # skip over '?'
        fs[n] = fs[n] or prep(one[n])  # ensure column 'n' compiles
        return fs[n](cell)  # compile column 'n'

    # --------------------------------------------------------
    one = next(src)
    fs = [None] * len(one)
    yield one
    for n, cells in enumerate(src):
        yield [ready(n, cell) for n, cell in enumerate(cells)]


if __name__ == "__main__":
    s = """
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
    
    for lst in cells(cols(rows(string(s)))):
        print(lst)
