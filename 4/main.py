from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

test_inp = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y)

    def pt_2_pair(self: Coord) -> Coord:
        return Coord(0 - self.x, self.y)


DIRECTIONS = [Coord(x, y) for x in range(-1, 2) for y in range(-1, 2)]

DIRECTIONS2 = [Coord(x, y) for x in range(-1, 2, 2) for y in range(-1, 2, 2)]


def parse_inp(inp: str) -> dict[Coord, str]:
    acc = {}
    for y, row in enumerate(inp.splitlines()):
        for x, letter in enumerate(row):
            acc[Coord(x, y)] = letter
    return acc


def pt1(inp: str) -> int:
    grid = parse_inp(inp)
    acc = 0
    for key in grid:
        if grid[key] == 'X':
            for d in DIRECTIONS:
                next_1 = key + d
                if next_1 in grid and grid[next_1] == 'M':
                    next_2 = next_1 + d
                    if next_2 in grid and grid[next_2] == 'A':
                        next_3 = next_2 + d
                        if next_3 in grid and grid[next_3] == 'S':
                            acc += 1
    return acc


def pt2(inp: str) -> int:
    grid = parse_inp(inp)
    acc = 0
    for key in grid:
        if grid[key] == 'A':
            for d in DIRECTIONS2:
                a = key + d
                b = key - d
                if (a in grid and grid[a] == 'M' and b in grid and grid[b] == 'S') or (
                    a in grid and grid[a] == 'S' and b in grid and grid[b] == 'M'
                ):
                    a1 = key + d.pt_2_pair()
                    a2 = key - d.pt_2_pair()
                    if (a1 in grid and grid[a1] == 'M' and a2 in grid and grid[a2] == 'S') or (
                        a1 in grid and grid[a1] == 'S' and a2 in grid and grid[a2] == 'M'
                    ):
                        acc += 1
    return acc / 4


assert pt1(test_inp) == 18
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 9
print(f'{pt2(inp) = }')
