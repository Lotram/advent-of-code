import json


def parse(obj):
    match obj:
        case dict():
            return sum(parse(val) for val in obj.values())
        case list():
            return sum(parse(val) for val in obj)
        case int():
            return obj
        case str():
            return 0


def part_1(text, example: bool = False):
    input_ = json.loads(text)
    result = parse(input_)
    return result


def parse_2(obj):
    match obj:
        case dict():
            if "red" in obj.values():
                return 0
            return sum(parse_2(val) for val in obj.values())
        case list():
            return sum(parse_2(val) for val in obj)
        case int():
            return obj
        case str():
            return 0


def part_2(text, example: bool = False):
    input_ = json.loads(text)
    result = parse_2(input_)
    return result
