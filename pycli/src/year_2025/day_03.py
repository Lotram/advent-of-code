def solve(text, size):
    result = 0

    for line in text.splitlines():
        values = [None] * size
        for idx, digit in enumerate(map(int, line)):
            length = len(line)
            for value_idx in range(size):
                if (
                    values[value_idx] is None or digit > values[value_idx]
                ) and idx <= length - (size - value_idx):
                    values[value_idx] = digit
                    values[value_idx + 1 :] = [None] * (size - value_idx - 1)
                    break

        result += int("".join(map(str, values)))
    return result


def part_1(text, example: bool = False):
    return solve(text, size=2)


def part_2(text, example: bool = False):
    return solve(text, size=12)
