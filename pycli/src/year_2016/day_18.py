def is_safe(left, right):
    return left == right


def get_row(prev):
    prev = [True, *prev, True]
    return [is_safe(prev[idx - 1], prev[idx + 1]) for idx in range(1, len(prev) - 1)]


def solution(prev, rounds):
    result = sum(prev)

    for _ in range(rounds):
        prev = get_row(prev)
        result += sum(prev)

    return result


def part_1(text, example: bool = False):
    prev = list(map(".".__eq__, text.strip()))
    rounds = 9 if len(prev) == 10 else 39
    return solution(prev, rounds)


def part_2(text, example: bool = False):
    prev = list(map(".".__eq__, text.strip()))
    rounds = 400000 - 1
    return solution(prev, rounds)
