from typing import *

class Cmd(NamedTuple):
    cmd: str
    data: int


def parse(lines: List[str]) -> List[Cmd]:
    return [Cmd(cmd=line.split(" ")[0], data=int(line.split(" ")[1])) for line in lines if len(line.split(" ")) >= 2]

def scores(data: List[Cmd]):
    x = 0
    y = 0
    aim = 0
    for line in data:
        if line.cmd == 'forward':
            x += line.data
            y += line.data * aim
        elif line.cmd == 'down':
#            y += line.data
            aim += line.data
        elif line.cmd == 'up':
 #           y -= line.data
            aim -= line.data
        else:
            print("warning: unknown command: " + str(line[0]))

    return [x, y]

def solution(data: List[str]) -> int:
    s = scores(parse(data))
    return s[0] * s[1]

import aoc
test_inp = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
test_out = 900
aoc.debug(solution, aoc.Level(2021, 2), (test_inp, test_out))