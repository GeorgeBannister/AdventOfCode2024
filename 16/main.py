from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

test_inp = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

test_inp_2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)


east = Coord(1, 0)
south = Coord(0, 1)
west = Coord(-1, 0)
north = Coord(0, -1)

MOVE_COST = 1
TURN_COST = 1000

direction_map = {east: (north, south), west: (north, south), north: (east, west), south: (east, west)}

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


def get_score(grid: Grid, start: Coord, end: Coord) -> int:
    # Curr, direction, score
    stack = [(start, east, 0, [start])]

    memory = {(start, east): 0}

    memory2 = []

    def cheaper(pos: Coord, direction: Coord, score: int) -> bool:
        tup = (pos, direction)
        if tup not in memory:
            return True
        if score <= memory[tup]:
            return True
        return False

    def enqueue_maybe(stack: list, pos: Coord, direction: Coord, score: int, path: list) -> None:
        if cheaper(pos, direction, score):
            memory[(pos, direction)] = score
            stack.append((pos, direction, score, path))

    while stack:
        new_stack = []
        for t in stack:
            curr, direction, score, path = t

            if curr == end:
                memory2.append((score, set(path)))
                continue

            forward_shadow = curr + direction
            if grid[forward_shadow] is None:
                new_path = list(path)
                new_path.append(forward_shadow)
                enqueue_maybe(new_stack, forward_shadow, direction, score + MOVE_COST, new_path)

            for new_d in direction_map[direction]:
                enqueue_maybe(new_stack, curr, new_d, score + TURN_COST, list(path))

        stack = new_stack

    curr_min = min(cost for tup, cost in memory.items() if tup[0] == end)
    acc = set()
    for x in memory2:
        if x[0] == curr_min:
            acc |= x[1]
    return curr_min, len(acc)


def pt1(inp: str) -> int:
    return get_score(*parse_inp(inp))[0]


def pt2(inp: str) -> int:
    return get_score(*parse_inp(inp))[1]


assert pt1(test_inp) == 7036
assert pt1(test_inp_2) == 11048
print(f'{pt1(inp) = }')
assert pt2(test_inp) == 45
assert pt2(test_inp_2) == 64
print(f'{pt2(inp) = }')
