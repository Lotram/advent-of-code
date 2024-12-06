j = 1j


def parse_text(text):
    rows = text.strip().splitlines()
    row_count = len(rows)
    col_count = len(rows[0])
    obstructions = set()
    for row_idx, line in enumerate(text.strip().splitlines()):
        for col_idx, char in enumerate(line):
            if char == "#":
                obstructions.add(col_idx + (row_count - row_idx - 1) * j)
            elif char == "^":
                start = col_idx + (row_count - row_idx - 1) * j

    return start, row_count, col_count, obstructions


def get_visited(start, row_count, col_count, obstructions):
    direction = j
    position = start
    visited = set()
    while 0 <= position.real < col_count and 0 <= position.imag < row_count:
        visited.add(position)
        position += direction
        while position + direction in obstructions:
            direction *= -j
    return visited


def part_1(text, example: bool = False):
    start, row_count, col_count, obstructions = parse_text(text)

    visited = get_visited(start, row_count, col_count, obstructions)

    result = len(visited)
    return result


# bruteforce solution
def part_2(text, example: bool = False):
    result = 0
    start, row_count, col_count, obstructions = parse_text(text)
    visited_positions = get_visited(start, row_count, col_count, obstructions)

    for candidate in visited_positions - {start}:
        _obstructions = obstructions | {candidate}
        position = start
        direction = j
        visited = set()
        while 0 <= position.real < col_count and 0 <= position.imag < row_count:
            if (position, direction) in visited:
                result += 1
                break

            visited.add((position, direction))
            position += direction
            while position + direction in _obstructions:
                direction *= -j

    return result
