from itertools import groupby


def solution(text, loop_count):
    result = text.strip()
    for _ in range(loop_count):
        result = "".join(
            f"{len(list(group))}{value}" for value, group in groupby(result)
        )

    return len(result)


def part_1(text):
    return solution(text, 40)


def part_2(text):
    return solution(text, 50)
