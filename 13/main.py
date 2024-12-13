from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

test_inp = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


@dataclass(slots=True)
class Machine:
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    prize_x: int
    prize_y: int

    def score_1(self: Machine) -> int:
        mat = np.array([[self.a_x, self.b_x], [self.a_y, self.b_y]])
        prize = np.array([[self.prize_x], [self.prize_y]])
        inv = np.linalg.inv(mat)
        res = inv @ prize
        a = np.round(res[0][0], decimals=3)
        b = np.round(res[1][0], decimals=3)

        if a % 1 == 0 and b % 1 == 0:
            return 3 * int(np.round(a)) + int(np.round(b))
        return 0


all_nums_re = re.compile(r'\d+', re.MULTILINE)


def parse_inp(inp: str) -> list[Machine]:
    return [Machine(*[int(x) for x in all_nums_re.findall(grp)]) for grp in inp.split('\n\n')]


def pt1(inp: str) -> int:
    return sum(m.score_1() for m in parse_inp(inp))


def pt2(inp: str) -> int:
    machines = parse_inp(inp)
    for m in machines:
        m.prize_x += 10000000000000
        m.prize_y += 10000000000000
    return sum(m.score_1() for m in machines)


assert pt1(test_inp) == 480
print(f'{pt1(inp) = }')
print(f'{pt2(inp) = }')
