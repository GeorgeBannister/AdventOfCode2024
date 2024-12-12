from __future__ import annotations

import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Collection, Iterator

test_inp = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

test_inp_2 = """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

test_inp_3 = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

test_inp_4 = """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

inp = (Path(__file__).parent / 'inp.txt').read_text()

type Region = set[Coord]
type Regions = list[Region]


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def adjacent(self: Coord, valid: Collection[Coord]) -> Iterator[Coord]:
        yield from (self + d for d in (Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)) if self + d in valid)

    def adjacent_all(self: Coord) -> Iterator[Coord]:
        yield from (self + d for d in (Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)))

    def diag_all(self: Coord) -> Iterator[Coord]:
        yield from (self + d for d in (Coord(1, 1), Coord(1, -1), Coord(-1, 1), Coord(-1, -1)))

    def is_corner(self: Coord, others: Collection[Coord], diag_not: Collection[Coord] = []) -> int:
        acc = 0
        for a, b in (
            (Coord(1, 0), Coord(0, -1)),
            (Coord(0, -1), Coord(-1, 0)),
            (Coord(-1, 0), Coord(0, 1)),
            (Coord(0, 1), Coord(1, 0)),
        ):
            if ((self + a) in others and (self + b) in others) and ((self + a + b) not in diag_not):
                acc += 1
        return acc


def parse_inp(inp: str) -> Regions:
    acc = []
    consumed = set()
    valid = {Coord(x, y): char for y, row in enumerate(inp.splitlines()) for x, char in enumerate(row)}
    for coord in valid:
        if coord not in consumed:
            co_val = valid[coord]
            consumed.add(coord)
            new_set = {coord}
            stack = [x for x in coord.adjacent(valid) if valid[x] == co_val]
            while stack:
                this = stack.pop()
                new_set.add(this)
                consumed.add(this)
                stack.extend([x for x in this.adjacent(valid) if valid[x] == co_val and x not in consumed])
            acc.append(new_set)
    return acc


def area(region: Region) -> int:
    return len(region)


def perimiter(region: Region) -> int:
    return sum((4 - len(list(x.adjacent(region)))) for x in region)


def sides(region: Region) -> int:
    neighbors = set()
    for x in region:
        for y in itertools.chain(x.adjacent_all(), x.diag_all()):
            if y not in region:
                neighbors.add(y)
    score = 0
    for neighbor in neighbors:
        score += neighbor.is_corner(region, diag_not=neighbors)
    for r in region:
        score += r.is_corner(neighbors)
    return score


def pt1(inp: str) -> int:
    return sum((area(x) * perimiter(x)) for x in parse_inp(inp))


def pt2(inp: str) -> int:
    return sum((area(x) * sides(x)) for x in parse_inp(inp))


assert pt1(test_inp) == 1930
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 1206
assert pt2(test_inp_2) == 368
assert pt2(test_inp_3) == 436
assert pt2(test_inp_4) == 236
print(f'{pt2(inp) = }')
