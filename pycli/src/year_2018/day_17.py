import re
from collections import defaultdict
from functools import cached_property
from itertools import count
from pathlib import Path

from pycli.src.grid import Vector2D as Vec


pattern = re.compile(
    r"(?P<axis_1>x|y)=(?P<val_1>\d+), (?P<axis_2>x|y)=(?P<range_start>\d+)..(?P<range_end>\d+)"
)


def parse(text):
    clay = set()
    lines = text.strip().split("\n")
    for match_ in map(pattern.match, lines):
        assert match_ is not None
        axis_1, val_1, axis_2, range_start, range_end = match_.groups()
        for val_2 in range(int(range_start), int(range_end) + 1):
            clay.add(Vec(**{axis_1: int(val_1), axis_2: val_2}))

    return clay


class Ground:
    def __init__(self, text):
        self.clay = parse(text)
        self.min_y = min(_clay.y for _clay in self.clay)
        self.max_y = max(_clay.y for _clay in self.clay)
        self.still_water = set()
        self.wet_sand = set()

    @cached_property
    def clay_by_x(self):
        _clay_by_x = defaultdict(set)
        for _clay in self.clay:
            _clay_by_x[_clay.x].add(_clay)

        return _clay_by_x

    def find_border(self, x, y, step=1) -> tuple[Vec, bool]:
        """
        looking for border at depth y
        """
        it = count(x, step)
        while True:
            _x = next(it)
            if Vec(_x + step, y) in self.clay:
                # border reached
                return Vec(_x, y), True
            elif Vec(_x + step, y + 1) not in self.clay | self.still_water:
                return Vec(_x + step, y), False

    def handle_source(self, source: Vec) -> set[Vec]:
        x = source.x
        try:
            y = min(
                clay_.y - 1
                for clay_ in self.clay_by_x[x] | self.still_water
                if clay_.y > source.y and clay_.x == x
            )
        except ValueError:
            self.wet_sand |= {
                Vec(x, _y)
                for _y in range(max(self.min_y, source.y + 1), self.max_y + 1)
            }

            return set()

        # still water blocks
        while True:
            left, has_left_border = self.find_border(x, y, step=-1)
            right, has_right_border = self.find_border(x, y, step=1)
            new_water_squares = {Vec(_x, y) for _x in range(left.x, right.x + 1)}
            assert not new_water_squares & self.clay
            if has_left_border and has_right_border:
                self.still_water |= new_water_squares
                y -= 1
            else:
                self.wet_sand |= new_water_squares | {
                    Vec(x, _y) for _y in range(max(self.min_y, source.y + 1), y)
                }
                return {
                    direction
                    for direction, border in (
                        (left, has_left_border),
                        (right, has_right_border),
                    )
                    if not border
                }


def print_grid(ground):
    min_x = min(_clay.x for _clay in ground.clay)
    max_x = max(_clay.x for _clay in ground.clay)
    _array = [
        ["." for _x in range(min_x - 1, max_x + 2)] for _y in range(ground.max_y + 2)
    ]
    _array[0][500 - min_x] = "+"
    from pycli.src.grid import Grid

    grid = Grid(_array)
    for _square in ground.clay:
        grid[(_square.y, _square.x - min_x)] = "#"
    for _square in ground.still_water:
        grid[(_square.y, _square.x - min_x)] = "~"

    for _square in ground.wet_sand - ground.still_water:
        grid[(_square.y, _square.x - min_x)] = "|"

    with Path("result_17.txt").open("w") as _file:
        grid.print(_file)


def part_1(text, example: bool = False):
    ground = Ground(text)
    sources = {Vec(500, 0)}
    visited = set()
    # print_grid(ground)
    while sources:
        source = sources.pop()
        visited.add(source)
        sources |= ground.handle_source(source) - visited
    # print_grid(ground)

    result = len(ground.wet_sand | ground.still_water)
    return result


def part_2(text, example: bool = False):
    ground = Ground(text)
    sources = {Vec(500, 0)}
    visited = set()
    # print_grid(ground)
    while sources:
        source = sources.pop()
        visited.add(source)
        sources |= ground.handle_source(source) - visited
    # print_grid(ground)

    result = len(ground.still_water)
    return result
