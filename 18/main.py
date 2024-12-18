from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Collection, Iterator

test_inp = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def adjacent(self: Coord, valid: Collection[Coord]) -> Iterator[Coord]:
        yield from (self + d for d in (Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)) if self + d in valid)


type Grid = dict[Coord, None | True]


def parse_inp(inp: str, end: Coord, n: int) -> Grid:
    acc = {}
    for x in range(end.x + 1):
        for y in range(end.y + 1):
            acc[Coord(x, y)] = None
    lines = iter(inp.splitlines())
    for _ in range(n):
        line = next(lines)
        l, r = line.split(',')
        acc[Coord(int(l), int(r))] = True
    return acc


def pt1(inp: str, end: Coord, n: int) -> int:
    start = Coord(0, 0)
    grid = parse_inp(inp, end, n)
    visited = {start}
    steps = 0
    bfs = [start]
    while True:
        steps += 1
        new_bfs = []
        for co in bfs:
            for adj in co.adjacent(grid):
                if grid[adj] is None and adj not in visited:
                    if adj == end:
                        return steps
                    visited.add(adj)
                    new_bfs.append(adj)
        bfs = new_bfs


class BreakOut(Exception): ...


def pt2(inp: str, end: Coord) -> str:
    acc = 1
    start = Coord(0, 0)
    while True:
        acc += 1
        grid = parse_inp(inp, end, acc)
        visited = {start}
        bfs = [start]
        try:
            while True:
                new_bfs = []
                for co in bfs:
                    for adj in co.adjacent(grid):
                        if grid[adj] is None and adj not in visited:
                            if adj == end:
                                raise BreakOut
                            visited.add(adj)
                            new_bfs.append(adj)
                if not new_bfs:
                    return inp.splitlines()[acc - 1]
                bfs = new_bfs
        except BreakOut:
            ...


assert pt1(test_inp, Coord(6, 6), 12) == 22
print(f'{pt1(inp, Coord(70,70), 1024) = }')
assert pt2(test_inp, Coord(6, 6)) == '6,1'
print(f'{pt2(inp, Coord(70,70)) = }')
