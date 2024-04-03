from functools import cache


def is_perpendicular(next_char, direction):
    return next_char == "-" and direction[0] or next_char == "|" and direction[1]


def is_parallel(next_char, direction):
    return next_char == "|" and direction[0] or next_char == "-" and direction[1]


def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return (t1[0] + t2[0], t1[1] + t2[1])


@cache
def get_next(char, position, direction):
    next_positions, next_directions = [], []

    match char:
        case ".":
            next_positions.append(add(position, direction))
            next_directions.append(direction)

        case "|" | "-":
            if is_parallel(char, direction):
                next_positions.append(add(position, direction))
                next_directions.append(direction)

            elif is_perpendicular(char, direction):
                for sign in [-1, 1]:
                    next_direction = (sign * direction[1], sign * direction[0])
                    next_directions.append(next_direction)
                    next_positions.append(add(position, next_direction))
            else:
                raise ValueError(char, direction)

        case "/":
            next_direction = (-direction[1], -direction[0])
            next_directions.append(next_direction)
            next_positions.append(add(position, next_direction))
        case "\\":
            next_direction = (direction[1], direction[0])
            next_directions.append(next_direction)
            next_positions.append(add(position, next_direction))

    return next_positions, next_directions


def parse(grid, start_position, start_direction):
    next_positions = [start_position]
    next_directions = [start_direction]
    visited = set()
    while True:
        if not next_positions:
            break

        positions, directions = next_positions, next_directions
        next_positions, next_directions = [], []

        for position, direction in zip(positions, directions):
            if not (0 <= position[0] < len(grid) and 0 <= position[1] < len(grid[0])):
                continue

            if (position, direction) in visited:
                continue

            visited.add((position, direction))

            char = grid[position[0]][position[1]]
            _next_positions, _next_directions = get_next(char, position, direction)
            next_positions.extend(_next_positions)
            next_directions.extend(_next_directions)

    return {position for position, _ in visited}


def part_1(text, example: bool = False):
    grid = tuple(tuple(line) for line in text.strip().split("\n"))
    visited = parse(grid, (0, 0), (0, 1))
    result = len(visited)
    return result


def part_2(text, example: bool = False):
    grid = tuple(tuple(line) for line in text.strip().split("\n"))
    start = [((idx, 0), (0, 1)) for idx in range(len(grid))]
    start += [((idx, len(grid[0]) - 1), (0, -1)) for idx in range(len(grid))]
    start += [((0, idx), (1, 0)) for idx in range(len(grid[0]))]
    start += [((len(grid) - 1, idx), (-1, 0)) for idx in range(len(grid[0]))]
    result = max(len(parse(grid, position, direction)) for position, direction in start)
    return result
