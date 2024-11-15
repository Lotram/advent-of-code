def part_1(text, example: bool = False):
    result = sum(int(line) // 3 - 2 for line in text.strip().splitlines())
    return result


def part_2(text, example: bool = False):
    result = 0
    for value in map(int, text.strip().splitlines()):
        total = 0
        while value // 3 - 2 > 0:
            value = value // 3 - 2
            total += value
        result += total

    return result
