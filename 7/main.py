import functools
import itertools
import operator
import re
from pathlib import Path

test_inp = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

inp = (Path(__file__).parent / 'inp.txt').read_text()

all_nums_re = re.compile(r'\d+')


def parse_inp(inp: str) -> list[tuple[int, list[int]]]:
    acc = []
    for line in inp.splitlines():
        nums = [int(x) for x in all_nums_re.findall(line)]
        lhs = nums[0]
        rhs = nums[1:]
        acc.append((lhs, rhs))
    return acc


def special_operator(a: int, b: int) -> int:
    return int(str(a) + str(b))


def score_from_row(l: tuple[int, list[int]], operators: list) -> int:
    lhs, rhs = l
    queue = [(rhs[0], rhs[1:])]
    while queue:
        acc, rs = queue.pop(0)
        for op in operators:
            acc2 = acc
            rs2 = list(rs)
            n = rs2.pop(0)
            acc2 = op(acc2, n)
            if acc2 == lhs and not rs2:
                return lhs
            if acc2 <= lhs and rs2:
                queue.append((acc2, rs2))
    return 0


def pt1(inp: str) -> int:
    lists = parse_inp(inp)
    acc = 0
    for l in lists:
        acc += score_from_row(l, [operator.add, operator.mul])
    return acc


def pt2(inp: str) -> int:
    lists = parse_inp(inp)
    acc = 0
    for l in lists:
        acc += score_from_row(l, [operator.add, operator.mul, special_operator])
    return acc


assert pt1(test_inp) == 3749
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 11387
print(f'{pt2(inp) = }')
