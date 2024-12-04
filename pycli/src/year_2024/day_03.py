import re


pattern = re.compile(r"(?:mul\((\d+),(\d+)\))")


def part_1(text, example: bool = False):
    result = sum(int(a) * int(b) for a, b in pattern.findall(text))
    return result


def part_2(text, example: bool = False):
    pattern = re.compile(r"(?:mul\((\d+),(\d+)\))|(do(?:n't)?)")
    enabled = True
    result = 0
    for x, y, action in pattern.findall(text):
        match (x, y, action):
            case (_, _, "do"):
                enabled = True
            case (_, _, "don't"):
                enabled = False
            case (x, y, _):
                if enabled:
                    result += int(x) * int(y)
    return result
