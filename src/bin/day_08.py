import json


def part_1(text):
    lines = text.strip().split("\n")
    result = sum(len(line) - len(eval(line)) for line in lines)

    return result


def part_2(text):
    lines = text.strip().split("\n")
    result = sum(len(json.dumps(line)) - len(line) for line in lines)
    return result
