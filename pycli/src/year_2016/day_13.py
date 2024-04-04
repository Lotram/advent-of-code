from functools import cache

from pycli.src.dijkstra import dijkstra
from pycli.src.grid import DIRECTIONS, Vector


@cache
def get_neighbour_func(extra):
    @cache
    def is_wall(x, y):
        return f"{x * x + 3 * x + 2 * x * y + y + y * y + extra:b}".count("1") % 2

    def _get_neighbours(node: Vector):
        for direction in DIRECTIONS:
            neighbour = node + direction
            if neighbour.row >= 0 and neighbour.col >= 0 and not is_wall(*neighbour):
                yield (neighbour, 1)

    return _get_neighbours


def part_1(text, example: bool = False):
    extra = int(text.strip())
    start = Vector(1, 1)
    end = Vector(7, 4) if extra == 10 else Vector(31, 39)
    result = dijkstra(start, end, get_neighbour_func(extra))
    return result[0]


def part_2(text, example: bool = False):
    extra = int(text.strip())
    start = Vector(1, 1)

    @cache
    def get_neighbours(node: Vector):
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
