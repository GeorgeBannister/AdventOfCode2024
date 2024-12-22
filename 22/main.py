import functools
from pathlib import Path

test_inp = """\
1
10
100
2024"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


@functools.cache
def iteration(secret: int) -> int:
    tmp = secret << 6
    secret = (tmp ^ secret) % 16777216
    tmp = secret >> 5
    secret = (tmp ^ secret) % 16777216
    tmp = secret << 11
    return (tmp ^ secret) % 16777216


def do_iters(inp: int, iters: int) -> int:
    for _ in range(iters):
        inp = iteration(inp)
    return inp


def pt1(inp: str) -> int:
    return sum(do_iters(int(x), 2000) for x in inp.splitlines())


def pt2(inp: str) -> int:
    return 0


assert pt1(test_inp) == 37327623
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 0
print(f'{pt2(inp) = }')
