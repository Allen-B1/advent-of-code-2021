from typing import *

def count2(inp: List[int]):
    windows = [inp[i] + inp[i+1] + inp[i+2] for i in range(len(inp)-2)]
#    print(windows)
    n = 0
    for i in range(len(windows)-1):
        if windows[i+1] > windows[i]:
            n += 1
    return n
    

def count(inp: List[int]):
    n = 0
    for i in range(len(inp)-1):
        if inp[i+1] > inp[i]:
            n += 1
    return n

def parse(inp: str) -> List[int]:
    return [int(s) for s in inp.split("\n") if s != ""]


if __name__ == "__main__":
    with open("input.txt") as f:
        s = f.read()
        l = parse(s)
        print(count(l))
        print(count2(l))
