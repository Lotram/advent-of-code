from functools import cache


@cache
def is_possible(available, pattern, part):
    func = sum if part == 2 else any
    if pattern == "":
        return 1
    return func(
        is_possible(available, pattern[len(a) :], part)
        for a in available
        if pattern.startswith(a)
    )


def parse(text):
    available, patterns = text.strip().split("\n\n")
    return tuple(
        sorted(available.split(", "), key=len, reverse=True)
    ), patterns.splitlines()


def part_1(text, example: bool = False):
    available, patterns = parse(text)

    result = sum(is_possible(available, pattern, 1) for pattern in patterns)
    return result


def part_2(text, example: bool = False):
    available, patterns = parse(text)

    result = sum(is_possible(available, pattern, 2) for pattern in patterns)
    return result
