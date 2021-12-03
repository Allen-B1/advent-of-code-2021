from typing import *
import os
import sys
import urllib.request

T = TypeVar('T')

Solution = Callable[[List[str]], T]

class Level(NamedTuple):
    year: int
    day: int

session = os.environ["AOC_SESSION"]
if session == None or session == "":
    sys.stderr.write("$AOC_SESSION not set\n")
    sys.exit(1)

def _fetch_real(level: Level) -> str:
    req = urllib.request.Request("https://adventofcode.com/%d/day/%d/input" % (level.year, level.day), method="GET")
    req.add_header("Cookie", "session="+session)
    resp = urllib.request.urlopen(req)
    return resp.read().decode('utf8')[:-1]

def get_real(level: Level) -> List[str]:
    """Returns the real input data for the given level"""
    try:
        with open(".cache/" + str(level.year) + "/real-" + str(level.day) + ".txt", "r") as f:
            return f.read().split("\n")
    except FileNotFoundError:
        s = _fetch_real(level)
        with open(".cache/" + str(level.year) + "/real-" + str(level.day) + ".txt", "w+") as f:
            f.write(s)
        return s.split("\n")

def debug(solution: Solution[T], level: Level, test: Optional[Tuple[str, T]] = None):
    if test is not None:
        test_out = solution(test[0].split("\n"))
        print("Test output: " + str(test_out))
        if test_out != test[1]:
            print("Incorrect")
            return

    real_out = solution(get_real(level))
    print("Real output: " + str(real_out))
