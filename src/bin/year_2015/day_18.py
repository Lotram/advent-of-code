from .grid import Grid, Point


def part_1(text, example: bool = False):
    grid = Grid(
        [[char == "#" for char in line] for line in text.strip().split("\n")], diag=True
    )
    cycles = 100
    for _ in range(cycles):
        new_arr = grid.arr.copy()
        for point, lit in grid.flat_iter():
            lit_neighbours = sum(_lit for _, _lit in grid.neighbours(point))
            new_arr[point] = lit_neighbours == 3 or (lit_neighbours == 2 and lit)

        grid.arr = new_arr

    result = sum(sum(grid))
    return result


def part_2(text, example: bool = False):
    grid = Grid(
        [[char == "#" for char in line] for line in text.strip().split("\n")], diag=True
    )
    cycles = 100
    corners = [
        Point(0, grid.col_size - 1),
        Point(0, 0),
        Point(grid.row_size - 1, 0),
        Point(grid.row_size - 1, grid.col_size - 1),
    ]

    for point in corners:
        grid[point] = True

    for _ in range(cycles):
        new_arr = grid.arr.copy()
        for point, lit in grid.flat_iter():
            lit_neighbours = sum(_lit for _, _lit in grid.neighbours(point))
            new_arr[point] = (
                lit_neighbours == 3 or (lit_neighbours == 2 and lit) or point in corners
            )

        grid.arr = new_arr

    result = sum(sum(grid))
    return result
