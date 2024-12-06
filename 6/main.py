from __future__ import annotations

import itertools
from dataclasses import dataclass
from pathlib import Path

test_inp = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y)


type Grid = dict[Coord, str]


inp = (Path(__file__).parent / 'inp.txt').read_text()


def parse_inp(inp: str) -> tuple[Grid, Coord]:
    acc = {}
    start = None
    for y, line in enumerate(inp.splitlines()):
        for x, char in enumerate(line):
            if char == '^':
                start = Coord(int(x), int(y))
                acc[Coord(int(x), int(y))] = '.'
            else:
                acc[Coord(int(x), int(y))] = char
    return acc, start


def pt1(inp: str) -> int:
    directions = itertools.cycle([Coord(0, -1), Coord(1, 0), Coord(0, 1), Coord(-1, 0)])
    grid, curr_pos = parse_inp(inp)
    visited = {curr_pos}
    count = 1
    current_delta = next(directions)
    while True:
        shadow = curr_pos + current_delta
        if shadow not in grid:
            print(f'{count = }')
            return count
        if grid[shadow] == '#':
            current_delta = next(directions)
            continue
        curr_pos = shadow
        if curr_pos not in visited:
            count += 1
        visited.add(curr_pos)


def get_visited_bar_start(inp: str) -> set[Coord]:
    directions = itertools.cycle([Coord(0, -1), Coord(1, 0), Coord(0, 1), Coord(-1, 0)])
    grid, curr_pos = parse_inp(inp)
    start = curr_pos
    visited = {curr_pos}
    current_delta = next(directions)
    while True:
        shadow = curr_pos + current_delta
        if shadow not in grid:
            visited.remove(start)
            return visited
        if grid[shadow] == '#':
            current_delta = next(directions)
            continue
        curr_pos = shadow
        visited.add(curr_pos)


def does_loop(inp: str, pos: Coord) -> bool:
    directions = itertools.cycle([Coord(0, -1), Coord(1, 0), Coord(0, 1), Coord(-1, 0)])
    grid, curr_pos = parse_inp(inp)
    grid[pos] = '#'
    current_delta = next(directions)
    positions_seen = {(curr_pos, current_delta)}
    while True:
        shadow = curr_pos + current_delta
        if shadow not in grid:
            return False
        if (shadow, current_delta) in positions_seen:
            return True
        if grid[shadow] == '#':
            current_delta = next(directions)
            continue
        curr_pos = shadow
        positions_seen.add((curr_pos, current_delta))


def pt2(inp: str) -> int:
    acc = 0
    for pos in get_visited_bar_start(inp):
        if does_loop(inp, pos):
            acc += 1
    return acc


assert pt1(test_inp) == 41
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 6
print(f'{pt2(inp) = }')
