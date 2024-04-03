from functools import cache

from .dijkstra import dijkstra
from .grid import DIRECTIONS, Point


@cache
def get_neighbour_func(extra):
    @cache
    def is_wall(x, y):
        return f"{x * x + 3 * x + 2 * x * y + y + y * y + extra:b}".count("1") % 2

    def _get_neighbours(node: Point):
        for direction in DIRECTIONS:
            neighbour = node + direction
            if neighbour.row >= 0 and neighbour.col >= 0 and not is_wall(*neighbour):
                yield (neighbour, 1)

    return _get_neighbours


def part_1(text, example: bool = False):
    extra = int(text.strip())
    start = Point(1, 1)
    end = Point(7, 4) if extra == 10 else Point(31, 39)
    result = dijkstra(start, end, get_neighbour_func(extra))
    return result[0]


def part_2(text, example: bool = False):
    extra = int(text.strip())
    start = Point(1, 1)

    @cache
    def get_neighbours(node: Point):
        return {neighbour[0] for neighbour in get_neighbour_func(extra)(node)}

    def get_nodes(n):
        if n == 0:
            return {start}
        n_1 = get_nodes(n - 1)
        result = set(n_1)
        for node in n_1:
            result |= set(get_neighbours(node))
        return result

    result = len(get_nodes(50))
    return result
