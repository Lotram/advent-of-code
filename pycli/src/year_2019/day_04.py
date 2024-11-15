from itertools import groupby


def part_1(text, example: bool = False):
    result = 0
    for value in range(*map(int, text.strip().split("-"))):
        digits = list(str(value))
        if all(digits[i] <= digits[i + 1] for i in range(5)) and any(
            digits[i] == digits[i + 1] for i in range(5)
        ):
            result += 1
    return result


def part_2(text, example: bool = False):
    result = 0
    for value in range(*map(int, text.strip().split("-"))):
        digits = list(str(value))
        if all(digits[i] <= digits[i + 1] for i in range(5)) and any(
            len(list(group)) == 2 for _, group in groupby(digits)
        ):
            result += 1
    return result
