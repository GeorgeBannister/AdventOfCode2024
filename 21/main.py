from __future__ import annotations

import functools
import re
from pathlib import Path
from typing import Any

from collections.abc import Iterable

from aoc_util import Coord, d

test_inp = """\
029A
980A
179A
456A
379A"""

type Keypad = dict[Coord, Any]


def manhattan_dist(a: Coord, b: Coord) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


MOVE_MAP = {
    Coord(0, 1): 'v',
    Coord(0, -1): '^',
    Coord(1, 0): '>',
    Coord(-1, 0): '<',
}

inp = (Path(__file__).parent / 'inp.txt').read_text()

nums_re = re.compile(r'\d+')

NUM_KEYPAD: Keypad = {
    Coord(0, 0): '7',
    Coord(1, 0): '8',
    Coord(2, 0): '9',
    Coord(0, 1): '4',
    Coord(1, 1): '5',
    Coord(2, 1): '6',
    Coord(0, 2): '1',
    Coord(1, 2): '2',
    Coord(2, 2): '3',
    Coord(0, 3): None,
    Coord(1, 3): '0',
    Coord(2, 3): 'A',
}

NUM_KEYPAD_MOVE_MAP = {
    x: [y for y in x.adjacent(NUM_KEYPAD) if NUM_KEYPAD[y] is not None] for x in NUM_KEYPAD if NUM_KEYPAD[x] is not None
}

DIRECTIONAL_KEYPAD: Keypad = {
    Coord(0, 0): None,
    Coord(1, 0): '^',
    Coord(2, 0): 'A',
    Coord(0, 1): '<',
    Coord(1, 1): 'v',
    Coord(2, 1): '>',
}

DIRECTIONAL_KEYPAD_MOVE_MAP = {
    x: [y for y in x.adjacent(DIRECTIONAL_KEYPAD) if DIRECTIONAL_KEYPAD[y] is not None]
    for x in DIRECTIONAL_KEYPAD
    if DIRECTIONAL_KEYPAD[x] is not None
}


KEYPADS = (NUM_KEYPAD, DIRECTIONAL_KEYPAD)
KEYPAD_MOVE_MAPS = (NUM_KEYPAD_MOVE_MAP, DIRECTIONAL_KEYPAD_MOVE_MAP)


def maybe_wrap(inp: str | Iterable[str]) -> Iterable[str]:
    if isinstance(inp, str):
        return (inp,)
    return inp


@functools.cache
def shortest_moves_to(curr_pos: Coord, sequence: str, hash_code: int) -> list[str] | str:
    if not sequence:
        return ''

    curr_goal = sequence[0]
    keypad = KEYPADS[hash_code]
    movemap = KEYPAD_MOVE_MAPS[hash_code]

    if keypad[curr_pos] == curr_goal:
        ret = shortest_moves_to(curr_pos, sequence[1:], hash_code)

        if isinstance(ret, str):
            ret = (ret,)

        return ['A' + x for x in ret]

    acc = []
    goal_coord = next(co for co in keypad if keypad[co] == curr_goal)
    man = manhattan_dist(curr_pos, goal_coord)

    for new_pos in movemap[curr_pos]:
        if manhattan_dist(new_pos, goal_coord) < man:
            ret = maybe_wrap(shortest_moves_to(new_pos, sequence, hash_code))
            acc.extend([MOVE_MAP[new_pos - curr_pos] + x for x in ret])
    return acc


def solve_code(code: str) -> int:
    set_1 = set(shortest_moves_to(Coord(2, 3), code, 0))
    m = 9999999999999
    for s in set_1:
        set_2 = set(shortest_moves_to(Coord(2, 0), s, 1))
        for pog in set_2:
            set_3 = set(shortest_moves_to(Coord(2, 0), pog, 1))
            for foo in set_3:
                m = min(m, len(foo))
    return get_score(code, m)


def get_score(code: str, l: int) -> int:
    num = nums_re.findall(code)[0]
    print(f'{num = }  {l = }')
    return int(num) * l


def pt1(inp: str) -> int:
    lines = inp.splitlines()

    acc = 0
    for l in lines:
        p = solve_code(l)

        print(f'{p = }')

        acc += p

    print(f'{acc = }')

    return acc


def pt2(inp: str) -> int:
    return 0


assert pt1(test_inp) == 126384
print('a1')
print(f'{pt1(inp) = }')
print(f'{pt2(inp) = }')
