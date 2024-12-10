from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Collection, Generator

test_inp = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

test_inp_2 = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y)

    def adjacent(self: Coord, valid: Collection[Coord]) -> Generator[Coord, None, None]:
        for delta in (Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)):
            shadow = self + delta
            if shadow in valid:
                yield shadow


type Trailheads = list[Coord]
type Grid = dict[Coord, int]


def parse_inp(inp: str) -> tuple[Grid, Trailheads]:
    trailheads = []
    grid = {}
    for y, row in enumerate(inp.splitlines()):
        for x, char in enumerate(row):
            co = Coord(x, y)
            i = int(char)
            if i == 0:
                trailheads.append(co)
            grid[co] = i
    return grid, trailheads


def valid_routes(trailhead: Coord, grid: Grid, pt_2=False) -> int:
    acc = 0
    queue = [x for x in trailhead.adjacent(grid) if grid[x] == 1]
    while queue:
        this_co = queue.pop(0)
        this_val = grid[this_co]
        if this_val == 9:
            acc += 1
            continue
        for adj in this_co.adjacent(grid):
            if grid[adj] == this_val + 1 and (pt_2 is True or adj not in queue):
                queue.append(adj)
    return acc


def pt1(inp: str) -> int:
    acc = 0
    grid, trailheads = parse_inp(inp)
    for trailhead in trailheads:
        acc += valid_routes(trailhead, grid)
    return acc


def pt2(inp: str) -> int:
    acc = 0
    grid, trailheads = parse_inp(inp)
    for trailhead in trailheads:
        acc += valid_routes(trailhead, grid, pt_2=True)
    return acc


assert pt1(test_inp) == 36
print(f'{pt1(inp) = }')
assert pt2(test_inp_2) == 81
print(f'{pt2(inp) = }')
