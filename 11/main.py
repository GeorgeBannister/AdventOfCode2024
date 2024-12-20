import functools
from pathlib import Path

test_inp = '125 17'

inp = (Path(__file__).parent / 'inp.txt').read_text()

type Stones = list[int]


def parse_inp(inp: str) -> Stones:
    return [int(x) for x in inp.split()]


@functools.cache
def n_child(inp: int, steps: int) -> int:
    if steps == 0:
        return 1
    s = str(inp)
    l = len(s)
    if inp == 0:
        return n_child(1, steps - 1)
    if l % 2 == 0:
        return n_child(int(s[: l // 2]), steps - 1) + n_child(int(s[l // 2 :]), steps - 1)
    return n_child(inp * 2024, steps - 1)


def n_steps(stones: Stones, steps: int) -> int:
    return sum(n_child(stone, steps) for stone in stones)


def pt1(inp: str) -> int:
    return n_steps(parse_inp(inp), 25)


def pt2(inp: str) -> int:
    return n_steps(parse_inp(inp), 75)


assert pt1(test_inp) == 55312
print(f'{pt1(inp) = }')
print(f'{pt2(inp) = }')
