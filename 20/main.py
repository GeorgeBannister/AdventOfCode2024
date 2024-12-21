from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Collection, Iterator

test_inp = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

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


def parse_inp(inp: str) -> tuple[Grid, Coord, Coord]:
    start = None
    end = None
    grid = {}

    for y, row in enumerate(inp.splitlines()):
        for x, char in enumerate(row):
            match char:
                case '#':
                    grid[Coord(x, y)] = True
                case '.':
                    grid[Coord(x, y)] = None
                case 'S':
                    grid[Coord(x, y)] = None
                    start = Coord(x, y)
                case 'E':
                    grid[Coord(x, y)] = None
                    end = Coord(x, y)
                case _:
                    raise RuntimeError

    return grid, start, end


def get_score(
    grid: Grid,
    start: Coord,
    end: Coord,
    cheats: Collection[Coord],
    stop_after: int = 10000,
) -> tuple[int, list[Coord]]:
    visited = {start}
    steps = 0
    bfs = [[start]]
    while True:
        steps += 1
        if steps > stop_after:
            return 9999999
        new_bfs = []
        for l in bfs:
            co = l[-1]
            for adj in co.adjacent(grid):
                if (grid[adj] is None or adj in cheats) and adj not in visited:
                    if adj == end:
                        return steps, [*l, adj]
                    visited.add(adj)
                    new_bfs.append([*l, adj])
        bfs = new_bfs


def manhattan_dist(a: Coord, b: Coord) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def solve(inp: str, target: int, cheat_n: int) -> int:
    grid, start, end = parse_inp(inp)
    base_score, path = get_score(grid, start, end, [])
    acc = 0
    for idx_a, val_a in enumerate(path):
        for idx_b, val_b in enumerate(path):
            man = manhattan_dist(val_a, val_b)
            if idx_b - idx_a >= man + target and man <= cheat_n:
                acc += 1
    return acc


assert solve(test_inp, target=38, cheat_n=2) == 3
print(f'{solve(inp, target=100, cheat_n=2) = }')
assert solve(test_inp, target=50, cheat_n=20) == 285
print(f'{solve(inp, target=100, cheat_n=20) = }')
