from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

test_inp = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y)


type Grid = dict[Coord, str]


def parse_inp(inp: str) -> Grid:
    return {Coord(x, y): char for y, row in enumerate(inp.splitlines()) for x, char in enumerate(row)}


def print_grid(grid, s: set):
    max_y = max(co.y for co in grid)
    max_x = max(co.x for co in grid)

    for y in range(max_y):
        for x in range(max_x):
            if Coord(x, y) in s:
                print('#', end='')
            else:
                print(grid[Coord(x, y)], end='')
        print()


def pt1(inp: str) -> int:
    grid = parse_inp(inp)
    acc = set()
    for key, val in grid.items():
        if val == '.':
            continue
        for key2, val2 in grid.items():
            if val == val2 and key != key2:
                delta = key2 - key
                shadow = key - delta
                if shadow in grid:
                    acc.add(shadow)
    return len(acc)


def pt2(inp: str) -> int:
    grid = parse_inp(inp)
    acc = set()
    for key, val in grid.items():
        if val == '.':
            continue
        acc.add(key)
        for key2, val2 in grid.items():
            if val == val2 and key != key2:
                delta = key2 - key
                keep_going = True
                shadow = key
                while keep_going:
                    shadow = shadow + delta
                    if shadow in grid:
                        acc.add(shadow)
                    else:
                        keep_going = False
    return len(acc)


assert pt1(test_inp) == 14
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 34
print(f'{pt2(inp) = }')
