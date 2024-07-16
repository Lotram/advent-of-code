from itertools import product, starmap

from pycli.src.grid import Vector2D

GRID_SIZE = 300

# 235,87,13


def compute_power_level(cell: Vector2D, serial_number):
    rack_id = cell.x + 10
    return ((rack_id * cell.y + serial_number) * rack_id % 1000) // 100 - 5


def get_square_value(summed_area, x, y, size):
    x0 = x - 1
    y0 = y - 1
    return (
        summed_area[Vector2D(x0 + size, y0 + size)]
        + summed_area.get(Vector2D(x0, y0), 0)
        - summed_area.get(Vector2D(x0, y0 + size), 0)
        - summed_area.get(Vector2D(x0 + size, y0), 0)
    )


def get_max(summed_area, size):
    return max(
        (get_square_value(summed_area, x, y, size), Vector2D(x, y))
        for x, y in product(range(1, GRID_SIZE + 1 - size), repeat=2)
    )


def build_summed_area(serial_number):
    cells = starmap(Vector2D, product(range(1, GRID_SIZE + 1), repeat=2))
    values = {cell: compute_power_level(cell, serial_number) for cell in cells}
    summed_area = {}
    for cell in starmap(Vector2D, product(range(1, GRID_SIZE + 1), repeat=2)):
        summed_area[cell] = (
            values[cell]
            + summed_area.get(cell - Vector2D(0, 1), 0)
            + summed_area.get(cell - Vector2D(1, 0), 0)
            - summed_area.get(cell - Vector2D(1, 1), 0)
        )

    return summed_area


def part_1(text, example: bool = False):
    serial_number = int(text.strip())
    summed_area = build_summed_area(serial_number)
    value, max_cell = get_max(summed_area, 3)
    result = f"{max_cell.x},{max_cell.y}"
    return result


# https://en.wikipedia.org/wiki/Summed-area_table
def part_2(text, example: bool = False):
    serial_number = int(text.strip())
    summed_area = build_summed_area(serial_number)
    max_value = 0
    for size in range(1, 300):
        value, cell = get_max(summed_area, size)
        if value > max_value:
            result = f"{cell.x},{cell.y},{size}"
            max_value = value

    return result
