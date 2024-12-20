from collections import deque

from pycli.src.grid import Grid


def build_path(grid):
    start = grid.find("S")
    end = grid.find("E")
    grid.replace("E", ".")
    grid.replace("S", ".")
    path = deque([start, start])
    while path[-1] != end:
        path.append(
            next(
                _position
                for _position, value in grid.neighbours(path[-1])
                if value == "." and _position != path[-2]
            )
        )

    path.popleft()
    return [complex(*position) for position in path]


def solve(path, min_goal, max_distance):
    all_directions = {
        idx: [
            complex(x, y)
            for x in range(-max_distance, max_distance + 1)
            for y in range(-max_distance, max_distance + 1)
            if abs(x) + abs(y) == idx
        ]
        for idx in range(1, max_distance + 1)
    }

    path_dict = {position: idx for idx, position in enumerate(path)}
    return sum(
        path_dict.get(position + direction, -1) >= idx + norm + min_goal
        for idx, position in enumerate(path[:-min_goal])
        for norm, _all_directions in all_directions.items()
        for direction in _all_directions
    )


def part_1(text, example: bool = False):
    grid = Grid.from_text(text)
    min_goal = 4 if example else 100
    path = build_path(grid)
    result = solve(path, min_goal, 2)
    return result


def part_2(text, example: bool = False):
    grid = Grid.from_text(text)
    min_goal = 50 if example else 100
    path = build_path(grid)
    result = solve(path.copy(), min_goal, 20)
    return result
