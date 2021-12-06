from typing import *
from collections import defaultdict

import aoc

LEVEL = aoc.Level(2021, 6)

TEST_DATA = """3,4,3,1,2"""

def iterate(d: Dict[int, int]) -> Dict[int, int]:
    new: Dict[int, int] = defaultdict(lambda: 0)
    for attr, freq in d.items():
        if attr == 0:
            new[8] += freq
            new[6] += freq
        else:
            new[attr-1] += freq
    return new

def parse(s: str) -> Dict[int, int]:
    d: Dict[int, int] = defaultdict(lambda: 0)
    for n in s.split(','):
        d[int(n)] += 1

    return d

def sol1(s: Sequence[str]) -> int:
    d = parse(s[0])
    for i in range(80):
        d = iterate(d)
    return sum([freq for freq in d.values()])

def sol2(s: Sequence[str]) -> int:
    d = parse(s[0])
    for i in range(256):
        d = iterate(d)
    return sum([freq for freq in d.values()])


aoc.debug(sol1, LEVEL, (TEST_DATA, 5934))
aoc.debug(sol2, LEVEL, (TEST_DATA, 26984457539))