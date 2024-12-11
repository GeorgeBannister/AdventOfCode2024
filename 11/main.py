import functools
from pathlib import Path

test_inp = '125 17'

inp = (Path(__file__).parent / 'inp.txt').read_text()

type Stones = list[int]


def parse_inp(inp: str) -> Stones:
    return [int(x) for x in inp.split()]


@functools.cache
def n_child(inp: int, n_steps_left: int) -> int:
    if n_steps_left == 0:
        return 1
    s = str(inp)
    l = len(s)
    if inp == 0:
        return n_child(1, n_steps_left - 1)
    if l % 2 == 0:
        return n_child(int(s[: (l // 2)]), n_steps_left - 1) + n_child(int(s[(l // 2) :]), n_steps_left - 1)
    return n_child(inp * 2024, n_steps_left - 1)


def n_steps(stones: Stones, steps: int) -> int:
    acc = 0
    for val in stones:
        acc += n_child(val, steps)
    return acc


def pt1(inp: str) -> int:
    stones = parse_inp(inp)
    return n_steps(stones, 25)


def pt2(inp: str) -> int:
    stones = parse_inp(inp)
    return n_steps(stones, 75)


assert pt1(test_inp) == 55312
print('A1')
print(f'{pt1(inp) = }')
print(f'{pt2(inp) = }')
