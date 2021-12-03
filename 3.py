from typing import *
import aoc

level = aoc.Level(2021, 3)
test_inp = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

# returns [most common, least common]
def stats(data: List[str]):
    n_1s = len([0 for c in data if c == "1"])
    n_0s = len([0 for c in data if c == "0"])
    if n_1s > n_0s: return [1, 0]
    if n_1s < n_0s: return [0, 1]
    return [1, 0]

def sol(inp: List[str]):
    gamma_bits = [0] * len(inp[0])
    ep_bits = [0] * len(inp[0])

    for i in range(len(gamma_bits)):
        all = [line[i] for line in inp]
        [gamma, ep] = stats(all)
        gamma_bits[i] = gamma
        ep_bits[i] = ep

    
    return int("".join(map(str, gamma_bits)), base=2) * int("".join(map(str, ep_bits)), base=2)

aoc.debug(sol, level, (test_inp, 198))

def rating(inp: List[str], type_: int) -> str:
    lines = list(inp)

    for i in range(len(inp[0])):
        stat = stats([line[i] for line in lines])

        lines = [line for line in lines if line[i] == str(stat[type_])]
        print (lines)

        if len(lines) == 1:
            print(lines[0])
            return lines[0]

    raise Exception("???")
    
def sol2(inp: List[str]):
    o = int(rating(inp, 0), base=2)
    c = int(rating(inp, 1), base=2)
    print(c, o)
    return c*o

aoc.debug(sol2, level, (test_inp, 230))