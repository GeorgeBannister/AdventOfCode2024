from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Collection, Iterator

test_inp = """\
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

    def adjacent(self: Coord, valid: Collection[Coord]) -> Iterator[Coord]:
        yield from (self + d for d in (Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)) if self + d in valid)


type Trailheads = list[Coord]
type Grid = dict[Coord, int]


def parse_inp(inp: str) -> tuple[Grid, Trailheads]:
    trailheads = []
    grid = {}
    for y, row in enumerate(inp.splitlines()):
        for x, char in enumerate(row):
            co = Coord(x, y)
            if char == '0':
                trailheads.append(co)
            grid[co] = int(char)
    return grid, trailheads


def valid_routes(trailhead: Coord, grid: Grid, pt_2=False) -> int:
    acc = 0
    queue = [x for x in trailhead.adjacent(grid) if grid[x] == 1]
    while queue:
        co = queue.pop(0)
        num = grid[co]
        if num == 9:
            acc += 1
            continue
        queue.extend([adj for adj in co.adjacent(grid) if grid[adj] == num + 1 and (pt_2 is True or adj not in queue)])
    return acc


def pt1(inp: str) -> int:
    grid, trailheads = parse_inp(inp)
    return sum(valid_routes(t, grid) for t in trailheads)


def pt2(inp: str) -> int:
    grid, trailheads = parse_inp(inp)
    return sum(valid_routes(t, grid, pt_2=True) for t in trailheads)


assert pt1(test_inp) == 36
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 81
print(f'{pt2(inp) = }')
