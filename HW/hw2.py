import re


# class Tbl:
#
# class Col:
#
# class Row:
#
#

def compiler(x):
    "return something that can compile strings of type x"
    try:
        int(x);
        return int
    except:
        try:
            float(x);
            return float
        except ValueError:
            return str


def string(s):
    "read lines from a string"
    for line in s.splitlines():
        yield line


def rows(src,
         sep=",",
         doomed=r'([\n\t\r ]|#.*)'):
    "convert lines into lists, killing whitespace and comments"
    for line in src:
        line = line.strip()
        line = re.sub(doomed, '', line)  # re.sub(pattern, repl, string, count=0, flags=0)
        if line:
            yield line.split(sep)


def cells(src):
    "convert strings into their right types"
    oks = None
    for n, cells in enumerate(src):
        if n == 0:
            yield cells
        else:
            oks = oks or [compiler(cell) for cell in cells]
            yield [f(cell) for f, cell in zip(oks, cells)]


def fromString(s):
    "putting it all together"
    for lst in cells(rows(string(s))):
        yield lst


def main():
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
    for lst in rows(string(s)):
        print(lst)


if __name__ == "__main__":
    main()
