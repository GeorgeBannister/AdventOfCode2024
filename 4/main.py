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


DIRECTIONS = [Coord(x, y) for x in range(-1, 2) for y in range(-1, 2)]

DIRECTIONS2 = [Coord(1, 1), Coord(1, -1)]


def parse_inp(inp: str) -> dict[Coord, str]:
    acc = {}
    for y, row in enumerate(inp.splitlines()):
        for x, letter in enumerate(row):
            acc[Coord(x, y)] = letter
    return acc


def pt1(inp: str) -> int:
    def direction_contains_xmas(centre: Coord, d: Coord) -> bool:
        for letter in 'MAS':
            centre = centre + d
            if centre not in grid or grid[centre] != letter:
                return False
        return True

    grid = parse_inp(inp)
    return len([key for key in grid if grid[key] == 'X' for d in DIRECTIONS if direction_contains_xmas(key, d)])


def pt2(inp: str) -> int:
    grid = parse_inp(inp)
    acc = 0
    for k in grid:
        if grid[k] == 'A':
            d1, d2 = DIRECTIONS2
            if (
                (k + d1 in grid and grid[k + d1] == 'M' and k - d1 in grid and grid[k - d1] == 'S')
                or (k + d1 in grid and grid[k + d1] == 'S' and k - d1 in grid and grid[k - d1] == 'M')
            ) and (
                (k + d2 in grid and grid[k + d2] == 'M' and k - d2 in grid and grid[k - d2] == 'S')
                or (k + d2 in grid and grid[k + d2] == 'S' and k - d2 in grid and grid[k - d2] == 'M')
            ):
                acc += 1
    return acc


assert pt1(test_inp) == 18
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 9
print(f'{pt2(inp) = }')
