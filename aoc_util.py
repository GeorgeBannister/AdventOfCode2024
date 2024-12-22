from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Collection, Iterator


def d(fun: Callable) -> Callable:
    """Annotation to help debug function calls"""

    def inner(*args, **kwargs):
        print(f'\033[38;5;200m+ {fun.__name__}\033[0m')
        l = locals()
        print(f'args = {l["args"]}')
        print(f'kwargs = {l["kwargs"]}')
        ret_val = fun(*args, **kwargs)
        print(f'{ret_val = }\n')
        return ret_val

    return inner


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y)

    def adjacent(self: Coord, valid: Collection[Coord]) -> Iterator[Coord]:
        yield from (self + d for d in (Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)) if self + d in valid)
