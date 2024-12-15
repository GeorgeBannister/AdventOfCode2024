from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

test_inp_small = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

test_inp = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

test_toy = """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

inp = (Path(__file__).parent / 'inp.txt').read_text()


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)


delta_map = {'^': Coord(0, -1), 'v': Coord(0, 1), '>': Coord(1, 0), '<': Coord(-1, 0)}

Wall = object()
Box = object()
Robot = object()
BoxLeft = object()
BoxRight = object()

type Grid = dict[Coord, Wall | Box | Robot | None]
type Grid2 = dict[Coord, Wall | BoxLeft | BoxRight | Robot | None]


def parse_inp(inp: str) -> tuple[Grid, str]:
    first, directions = inp.split('\n\n')
    grid = {}
    for y, row in enumerate(first.splitlines()):
        for x, char in enumerate(row):
            co = Coord(x, y)
            match char:
                case '.':
                    grid[co] = None
                case '#':
                    grid[co] = Wall
                case '@':
                    grid[co] = Robot
                case 'O':
                    grid[co] = Box
                case _:
                    raise RuntimeError
    return grid, directions.strip().replace('\n', '')


def parse_inp_2(inp: str) -> tuple[Grid2, str]:
    first, directions = inp.split('\n\n')

    first_ammended = ''

    for char in first:
        if char == '#':
            first_ammended += '##'
        if char == 'O':
            first_ammended += '[]'
        if char == '.':
            first_ammended += '..'
        if char == '@':
            first_ammended += '@.'
        if char == '\n':
            first_ammended += '\n'

    grid = {}
    for y, row in enumerate(first_ammended.splitlines()):
        for x, char in enumerate(row):
            co = Coord(x, y)
            match char:
                case '.':
                    grid[co] = None
                case '#':
                    grid[co] = Wall
                case '@':
                    grid[co] = Robot
                case '[':
                    grid[co] = BoxLeft
                case ']':
                    grid[co] = BoxRight
                case _:
                    raise RuntimeError
    return grid, directions.strip().replace('\n', '')


def get_score(grid: Grid) -> int:
    return sum(bla.x + bla.y * 100 for bla in grid if grid[bla] is Box)


def get_score_2(grid: Grid2) -> int:
    return sum(bla.x + bla.y * 100 for bla in grid if grid[bla] is BoxLeft)


def move(grid: Grid, delta: Coord) -> None:
    curr_pos = next(x for x in grid if grid[x] is Robot)
    robot_shadow = curr_pos + delta

    if grid[robot_shadow] is Wall:
        return

    if grid[robot_shadow] is None:
        grid[curr_pos] = None
        grid[robot_shadow] = Robot
        return

    if grid[robot_shadow] is Box:
        shadow_grid = dict(grid)
        shadow_grid[curr_pos] = None
        shadow_grid[robot_shadow] = Robot

        box_old_pos = robot_shadow
        while True:
            box_old_pos = box_old_pos + delta
            if shadow_grid[box_old_pos] is None:
                shadow_grid[box_old_pos] = Box
                for x in grid:
                    grid[x] = shadow_grid[x]
                return
            if shadow_grid[box_old_pos] is Wall:
                return


# Map a Coord to what it will become if move is successful
type PendingMove = tuple[Coord, None | Robot | BoxLeft | BoxRight]


def move_2(grid: Grid, delta: Coord) -> None:
    curr_pos = next(x for x in grid if grid[x] is Robot)
    robot_shadow = curr_pos + delta

    if grid[robot_shadow] is Wall:
        return

    if grid[robot_shadow] is None:
        grid[curr_pos] = None
        grid[robot_shadow] = Robot
        return

    pending: list[PendingMove] = []
    visited = set()

    def add_tile(tile: Coord, delta: Coord) -> bool:
        if tile in visited:
            return True
        visited.add(tile)
        if grid[tile] is BoxLeft and not add_tile(tile + Coord(1, 0), delta):
            return False
        if grid[tile] is BoxRight and not add_tile(tile + Coord(-1, 0), delta):
            return False
        shadow = tile + delta
        pending.append((shadow, grid[tile]))
        pending.append((tile, None))
        if grid[shadow] is Wall:
            return False
        if grid[shadow] is None:
            return True

        if not add_tile(shadow, delta):
            return False
        return True

    if not add_tile(robot_shadow, delta):
        return

    for idx in range(len(pending) - 1, -1, -1):
        co, t = pending[idx]
        if t is None:
            indexes = [idx for idx in range(len(pending)) if pending[idx][0] == co]
            indexes.remove(idx)
            if len(indexes):
                pending.pop(idx)

    for p in pending:
        co, t = p
        grid[co] = t

    grid[robot_shadow] = Robot
    grid[curr_pos] = None

    return


def print_grid(grid: Grid | Grid2) -> None:
    max_x = max(g.x for g in grid)
    max_y = max(g.y for g in grid)

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            co = Coord(x, y)
            if grid[co] is Wall:
                print('#', end='')
            elif grid[co] is None:
                print('.', end='')
            elif grid[co] is Robot:
                print('@', end='')
            elif grid[co] is Box:
                print('O', end='')
            elif grid[co] is BoxLeft:
                print('[', end='')
            elif grid[co] is BoxRight:
                print(']', end='')
            else:
                raise RuntimeError(f'{grid[co] = }')
        print('')


def pt1(inp: str) -> int:
    grid, directions = parse_inp(inp)
    for char in directions:
        move(grid, delta_map[char])

    return get_score(grid)


def pt2(inp: str) -> int:
    grid, directions = parse_inp_2(inp)
    for char in directions:
        move_2(grid, delta_map[char])

    return get_score_2(grid)


assert pt1(test_inp_small) == 2028
assert pt1(test_inp) == 10092
print(f'{pt1(inp) = }')
assert pt2(test_toy) == (105 + 207 + 306)
assert pt2(test_inp) == 9021
print(f'{pt2(inp) = }')
