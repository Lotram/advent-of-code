from typing import NamedTuple

valid_to = {
    "7": [(0, -1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
    "F": [(0, 1), (1, 0)],
    "L": [(0, 1), (-1, 0)],
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
}


def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return tuple(a + b for a, b in zip(t1, t2))


def get_positions(lines):
    start_row = None
    start_col = None
    for row, line in enumerate(lines):
        try:
            col = line.index("S")
        except:
            continue
        else:
            start_row, start_col = row, col
            break

    assert start_row is not None
    assert start_col is not None
    current_position = (start_row, start_col)
    positions = [current_position]

    def get_first_direction() -> tuple[str, tuple[int, int]]:
        for row_idx, col_idx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (
                start_row + row_idx < 0
                or start_col + col_idx < 0
                or (char := lines[start_row + row_idx][start_col + col_idx]) == "."
            ):
                continue
            if (-row_idx, -col_idx) in valid_to[char]:
                return (char, (row_idx, col_idx))

        assert False

    cur_char, going_to = get_first_direction()
    current_position = add(going_to, current_position)
    positions.append(current_position)

    def get_next_dir(char, row, column):
        return next(
            going_to for going_to in valid_to[char] if going_to != (-row, -column)
        )

    while True:
        going_to = get_next_dir(cur_char, *going_to)
        current_position = add(going_to, current_position)
        cur_char = lines[current_position[0]][current_position[1]]
        if cur_char == "S":
            break
        positions.append(current_position)
    return positions


def part_1(text):
    lines = [list(line) for line in text.split("\n") if line]
    positions = get_positions(lines)
    return len(positions) / 2


class Position(NamedTuple):
    row: int
    column: int


def part_2(text):
    lines = [list(line) for line in text.split("\n") if line]
    positions = [Position(*position) for position in get_positions(lines)]
    char_by_pos = {pos: lines[pos.row][pos.column] for pos in positions}
    counter = 0
    for row in range(0, len(lines)):
        inside = False
        last_char = None
        for col in range(0, len(lines[0])):
            char = char_by_pos.get(Position(row, col))
            match char:
                case "|":
                    inside = not inside
                case "L":
                    last_char = "L"
                case "F":
                    last_char = "F"
                case "J":
                    if last_char == "F":
                        inside = not inside
                    last_char = None
                case "7":
                    if last_char == "L":
                        inside = not inside
                    last_char = None

                case None:
                    if inside:
                        counter += 1

    return counter
