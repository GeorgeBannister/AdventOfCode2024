import functools
from pathlib import Path

test_inp = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


def parse_inp(inp: str) -> tuple[frozenset[str], list[str]]:
    one, two = inp.split('\n\n')
    return frozenset({x.strip() for x in one.split(',')}), two.splitlines()


@functools.cache
def possible(goal: str, valid: frozenset) -> bool:
    if not goal:
        return True

    return any(possible(goal[len(x) :], valid) for x in valid if goal.startswith(x))


@functools.cache
def cnt(goal: str, valid: frozenset) -> bool:
    if not goal:
        return 1

    return sum(cnt(goal[len(x) :], valid) for x in valid if goal.startswith(x))


def pt1(inp: str) -> int:
    acc = 0
    ingredients, goals = parse_inp(inp)
    for g in goals:
        if possible(g, ingredients):
            acc += 1
    return acc


def pt2(inp: str) -> int:
    acc = 0
    ingredients, goals = parse_inp(inp)
    for g in goals:
        acc += cnt(g, ingredients)
    return acc


assert pt1(test_inp) == 6
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 16
print(f'{pt2(inp) = }')
