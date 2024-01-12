from .dijkstra import matrix_dijkstra


def neighbours(grid, row, col):
    _neighbours = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]
    return [
        ((_row, _column), 1)
        for _row, _column in _neighbours
        if 0 <= _row < len(grid)
        and 0 <= _column < len(grid[0])
        and ord(grid[_row, _column]) >= ord(grid[row, col]) - 1
    ]


class Grid(list):
    def __getitem__(self, item):
        if isinstance(item, tuple) and len(item) == 2:
            return self.__getitem__(item[0])[item[1]]

        return super().__getitem__(item)

    def __setitem__(self, item, value):
        if isinstance(item, tuple) and len(item) == 2:
            return self.__getitem__(item[0]).__setitem__(item[1], value)

        return super().__setitem__(item, value)

    def find(self, item):
        return next(
            (row, col)
            for row, line in enumerate(self)
            for col, char in enumerate(line)
            if char == item
        )

    def find_all(self, item):
        return [
            (row, col)
            for row, line in enumerate(self)
            for col, char in enumerate(line)
            if char == item
        ]


def part_1(text):
    grid = Grid(list(line) for line in text.strip().split("\n"))
    start = grid.find("S")
    end = grid.find("E")
    grid[start] = "a"
    grid[end] = "z"
    dist, path = matrix_dijkstra(grid, end, start, neighbour_function=neighbours)
    return dist


def part_2(text):
    grid = Grid(list(line) for line in text.strip().split("\n"))
    start = grid.find("S")
    end = grid.find("E")
    grid[start] = "a"
    grid[end] = "z"
    distances = matrix_dijkstra(grid, end, None, neighbour_function=neighbours)
    candidates = grid.find_all("a")
    return min(distances[candidate] for candidate in candidates)
