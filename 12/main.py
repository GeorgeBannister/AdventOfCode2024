from __future__ import annotations

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


def pt1(inp: str) -> int:
    regions = parse_inp(inp)
    return sum((area(x) * perimiter(x)) for x in regions)


def pt2(inp: str) -> int:
    return 0


assert pt1(test_inp) == 1930
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 0
print(f'{pt2(inp) = }')
