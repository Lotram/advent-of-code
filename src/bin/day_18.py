from collections import Counter

from PIL import Image, ImageDraw


def parse_line(line):
    direction, value, color = line.split()

    return direction, int(value), color[2:-1]


black = (0, 0, 0)
white = (255, 255, 255)


def build_grid(lines, width, height):
    grid = [[white for _ in range(width + 1)] for _ in range(height + 1)]
    row, col = int(height / 2), int(width / 2)
    for dir, value, _ in lines:
        match dir:
            case "R":
                for idx in range(0, value):
                    grid[row][col + 1 + idx] = black
                col += value
            case "L":
                for idx in range(0, value):
                    grid[row][col - (1 + idx)] = black
                col -= value
            case "U":
                for idx in range(0, value):
                    grid[row - (idx + 1)][col] = black
                row -= value
            case "D":
                for idx in range(0, value):
                    grid[row + (idx + 1)][col] = black
                row += value

    return grid


def compute_area(points):
    return 0.5 * sum(
        points[idx][0] * points[idx + 1][1] - points[idx][1] * points[idx + 1][0]
        for idx in range(len(points) - 1)
    )


def get_turn(previous_dir, dir):
    if (previous_dir, dir) in {("U", "R"), ("R", "D"), ("D", "L"), ("L", "U")}:
        return "r"
    elif (previous_dir, dir) in {("U", "L"), ("L", "D"), ("D", "R"), ("R", "U")}:
        return "l"
    else:
        raise ValueError("invalid turn", previous_dir, dir)


def part_1(text):
    lines = [parse_line(line) for line in text.strip().split("\n")]
    turns = []
    previous_direction = lines[-1][0]
    for dir, value, _ in lines:
        turn = get_turn(previous_direction, dir)
        turns.append((turn, dir, value))
        previous_direction = dir

    main_direction = Counter([t[0] for t in turns]).most_common(1)[0][0]

    points = []
    row, col = (0, 0)
    for idx, (turn, dir, value) in enumerate(turns):
        extra = (
            (turn == main_direction)
            + (turns[(idx + 1) % len(turns)][0] == main_direction)
            - 1
        )
        length = value + extra
        match dir:
            case "R":
                col += length
            case "L":
                col -= length
            case "U":
                row -= length
            case "D":
                row += length
        points.append((row, col))

    result = abs(int(compute_area(points)))
    return result


def parse_line_2(line):
    _, _, color = line.split()

    value = int(color[2:-2], 16)
    directions = {"0": "R", "1": "D", "2": "L", "3": "U"}

    return directions[color[-2]], value, color[2:-1]


def part_2(text):
    lines = [parse_line_2(line) for line in text.strip().split("\n")]
    sizes = {"R": 0, "L": 0, "U": 0, "D": 0}
    turns = []
    previous_direction = lines[-1][0]
    for dir, value, _ in lines:
        sizes[dir] += value
        turn = get_turn(previous_direction, dir)
        turns.append((turn, dir, value))
        previous_direction = dir

    main_direction = Counter([t[0] for t in turns]).most_common(1)[0][0]

    points = []
    row, col = (0, 0)
    for idx, (turn, dir, value) in enumerate(turns):
        extra = (
            (turn == main_direction)
            + (turns[(idx + 1) % len(turns)][0] == main_direction)
            - 1
        )
        length = value + extra
        match dir:
            case "R":
                col += length
            case "L":
                col -= length
            case "U":
                row -= length
            case "D":
                row += length
        points.append((row, col))

    result = abs(int(compute_area(points)))
    return result
