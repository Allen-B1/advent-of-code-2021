from typing import *

import aoc

LEVEL = aoc.Level(2021, 5)

TEST_DATA = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

class Line(NamedTuple):
    p1: Tuple[int, int]
    p2: Tuple[int, int]

def parse(inp: Sequence[str]) -> List[Line]:
    ptstrs = [[p.strip() for p in l.split("->")] for l in inp if l != ""]
    return [
        Line(
            cast(Tuple[int, int], tuple(int(n) for n in ptstr[0].split(","))),
            cast(Tuple[int, int], tuple(int(n) for n in ptstr[1].split(","))),
        )
        for ptstr in ptstrs if ptstr != ""]

SIZE = 1000
def coords(x: int, y: int) -> int:
    return y*SIZE+x

T = TypeVar('T')
def printboard(b: Sequence[T]):
    for y in range(SIZE):
        print(" ".join([str(b[y*SIZE+x]) for x in range(SIZE)]))
import math
def sgn(n: int) -> int:
    return 1 if n > 0 else (0 if n == 0 else  -1)

def sol2(inp: Sequence[str]):
    lines = parse(inp)
    board = [0] * SIZE*SIZE
    for line in lines:
        if line.p1[0] == line.p2[0]:
            for y in range(min(line.p1[1], line.p2[1]), max(line.p1[1], line.p2[1])+1):
                board[coords(line.p1[0], y)] += 1
        elif line.p1[1] == line.p2[1]:
            for x in range(min(line.p1[0], line.p2[0]), max(line.p1[0], line.p2[0])+1):
                board[coords(x, line.p1[1])] += 1
        else:
            if sgn(line.p1[0]-line.p2[0]) == sgn(line.p1[1]-line.p2[1]):
                # forward
                x = min(line.p1[0], line.p2[0])
                for y in range(min(line.p1[1], line.p2[1]), max(line.p1[1], line.p2[1])+1):
                    board[coords(x, y)] += 1
                    x += 1
            else:
                # backwards
                x = max(line.p1[0], line.p2[0])
                for y in range(min(line.p1[1], line.p2[1]), max(line.p1[1], line.p2[1])+1):
                    board[coords(x, y)] += 1
                    x -= 1
#    printboard(board)
    return len([1 for c in board if c >= 2])

aoc.debug(sol2, LEVEL, (TEST_DATA, 12))