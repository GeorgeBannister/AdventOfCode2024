from __future__ import annotations

import re
from dataclasses import dataclass
from functools import reduce
from pathlib import Path

test_inp = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


@dataclass
class Robot:
    p_x: int
    p_y: int
    v_x: int
    v_y: int

    def step(self: Robot, width: int, height: int) -> None:
        self.p_x = (self.p_x + self.v_x) % width
        self.p_y = (self.p_y + self.v_y) % height

    def in_bounds(self: Robot, w_from: int, w_to: int, h_from: int, h_to: int) -> bool:
        return (w_from <= self.p_x < w_to) and (h_from <= self.p_y < h_to)


all_nums_re = re.compile(r'-?\d+')


def parse_inp(inp: str) -> list[Robot]:
    return [Robot(*[int(x) for x in all_nums_re.findall(line)]) for line in inp.splitlines()]


def get_score(robots: list[Robot], width: int, height: int) -> int:
    half_w = width // 2
    half_h = height // 2
    acc = []
    for quad in (
        (0, half_w, 0, half_h),
        (half_w + 1, width, 0, half_h),
        (0, half_w, half_h + 1, height),
        (half_w + 1, width, half_h + 1, height),
    ):
        acc.append([r.in_bounds(*quad) for r in robots].count(True))
    return reduce(lambda a, b: a * b, acc, 1)


def pt1(inp: str, width: int = 101, height: int = 103) -> int:
    robots = parse_inp(inp)

    for _ in range(100):
        for robot in robots:
            robot.step(width, height)

    return get_score(robots, width, height)


def pt2(inp: str) -> int:
    return 0


assert pt1(test_inp, 11, 7) == 12
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 0
print(f'{pt2(inp) = }')
