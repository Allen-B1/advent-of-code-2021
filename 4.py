from typing import *
import aoc

LEVEL = aoc.Level(2021, 4)

class Board(NamedTuple):
    nums: Sequence[int]

class Data(NamedTuple):
    draws: Sequence[int]
    boards: Sequence[Board]

def parse(items: Sequence[str]) -> Data:
    boards = "\n".join(items).split("\n\n")
    nums = tuple(map(int, boards[0].split(",")))
    boards_ = [Board(tuple(int(i) for i in board.split())) for board in boards[1:]]
    return Data(nums, boards_)

def board_score(nums: Sequence[int], board: Board) -> int:
    drawn = [False] * 25
    nums_ = set(nums)

    for i, board_num in enumerate(board.nums):
        if board_num in nums_:
            drawn[i] = True

    # bingo?
    bingo = False
    # horizontal
    for i in range(5):
        if all([drawn[j] for j in range(5*i, 5*i+5)]):
            print("h" + str(i))
            bingo = True
    
    for i in range(5):
        if all([drawn[j] for j in range(i, 25, 5)]):
            print("v"+str(i))
            bingo = True
    """
    if all([drawn[i*5+i] for i in range(5)]):
        print("d1")
        bingo = True

    if all([drawn[i*5+(4-i)] for i in range(5)]):
        print("d2")
        bingo = True
    """

    # calculate score
    if not bingo:
        return 0

    s = sum([board.nums[i] for i, is_drawn in enumerate(drawn) if not is_drawn])
#    print("sum:", s)
#    print("nums:", nums)
    return s * nums[len(nums)-1]

def sol1(inp: Sequence[str]) -> int:
    data = parse(inp)
    for i in range(len(data.draws)):
        for board in data.boards:
            score = board_score(data.draws[:i], board)
            if score != 0:
#                print(data.draws[:i])
#                print(board)
                return score
    return 0

def sol2(inp: Sequence[str]) -> int:
    data = parse(inp)
    done: Set[int] = set()
    for i in range(len(data.draws)):
        for board_num, board in enumerate(data.boards):
            score = board_score(data.draws[:i], board)
            if score != 0 and board_num not in done:
                if len(done) == len(data.boards) - 1:
                    print(done)
                    return score
                done.add(board_num)
    return 0


test_data = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""
aoc.debug(sol1, LEVEL, (test_data, 4512))
aoc.debug(sol2, LEVEL, (test_data, 1924))