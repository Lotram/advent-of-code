import re


pattern = re.compile(r"(-?\d+)")


def predict(values):
    lines = [values]
    while True:
        next_line = [values[i + 1] - values[i] for i in range(len(values) - 1)]
        lines.append(next_line)
        if all(val == next_line[0] for val in next_line[1:]):
            return sum(line[-1] for line in lines)
        values = next_line


def part_1(text, example: bool = False):
    lines = text.split("\n")
    return sum(predict(list(map(int, pattern.findall(line)))) for line in lines if line)


def predict_2(values):
    lines = [values]
    while True:
        next_line = [values[i + 1] - values[i] for i in range(len(values) - 1)]
        lines.append(next_line)
        if all(val == next_line[0] for val in next_line[1:]):
            return sum(line[0] * (-1) ** idx for idx, line in enumerate(lines))
        values = next_line


def part_2(text, example: bool = False):
    lines = text.split("\n")
    return sum(
        predict_2(list(map(int, pattern.findall(line)))) for line in lines if line
    )
