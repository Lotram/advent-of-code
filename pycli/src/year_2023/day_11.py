from itertools import combinations
from typing import NamedTuple


class Position(NamedTuple):
    row: int
    column: int


def get_positions(lines):
    positions = []
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            if char == "#":
                positions.append(Position(row_idx, col_idx))
    return positions


def get_ordered_values(a, b):
    return (a, b) if a < b else (b, a)


def expanded_count(expanded_set, start_val, end_val, length) -> int:
    min_val, max_val = get_ordered_values(start_val, end_val)
    rows_to_cross = set(range(min_val, max_val))
    return len(expanded_set & rows_to_cross) * length


def get_answer(lines, expand_length):
    row_length = len(lines[0])
    expanded_rows = set(
        idx for idx, line in enumerate(lines) if all(char == "." for char in line)
    )
    expanded_columns = set(
        col for col in range(row_length) if all(line[col] == "." for line in lines)
    )
    positions = get_positions(lines)
    total_distance = 0
    for start_pair, end_pair in combinations(positions, 2):
        total_distance += abs(end_pair.row - start_pair.row) + abs(
            end_pair.column - start_pair.column
        )
        total_distance += expanded_count(
            expanded_rows, start_pair.row, end_pair.row, expand_length - 1
        )
        total_distance += expanded_count(
            expanded_columns, start_pair.column, end_pair.column, expand_length - 1
        )
    return total_distance


def part_1(text, example: bool = False):
    expand_length = 2
    lines = [list(line) for line in text.strip().split("\n")]
    result = get_answer(lines, expand_length)
    return result


def part_2(text, example: bool = False):
    expand_length = 1_000_000
    lines = [list(line) for line in text.strip().split("\n")]
    result = get_answer(lines, expand_length)
    return result
