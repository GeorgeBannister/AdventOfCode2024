from itertools import pairwise
from pathlib import Path

test_inp = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


def parse_inp(inp: str) -> list[list[int]]:
    return [[int(x) for x in line.split()] for line in inp.splitlines()]


def safe_1(l: list[int]) -> bool:
    def ok_1(i: tuple[int, int]) -> bool:
        return 1 <= (i[0] - i[1]) <= 3

    def ok_2(i: tuple[int, int]) -> bool:
        return -1 >= (i[0] - i[1]) >= -3

    return all(ok_1(x) for x in pairwise(l)) or all(ok_2(x) for x in pairwise(l))


def pt1(inp: str) -> int:
    acc = 0
    lists = parse_inp(inp)
    for l in lists:
        if safe_1(l):
            acc += 1
    return acc


def pt2(inp: str) -> int:
    acc = 0
    lists = parse_inp(inp)
    for l in lists:
        tmp_lists = [list(l)]
        for x in range(len(l)):
            new_l = list(l)
            new_l.pop(x)
            tmp_lists.append(new_l)
        if any(safe_1(x) for x in tmp_lists):
            acc += 1
    return acc


assert pt1(test_inp) == 2
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 4
print(f'{pt2(inp) = }')
