import functools


def parse(text):
    _rules, _updates = text.strip().split("\n\n")
    rules = set(_rules.splitlines())
    updates = [update.split(",") for update in _updates.splitlines()]

    def compare(x, y):
        return -1 if f"{x}|{y}" in rules else 1

    return compare, updates


def part_1(text, example: bool = False):
    compare, updates = parse(text)

    correct_updates = (
        update
        for update in updates
        if all(
            compare(update[idx], update[idx + 1]) == -1
            for idx in range(len(update) - 1)
        )
    )
    result = sum(int(update[len(update) // 2]) for update in correct_updates)
    return result


def part_2(text, example: bool = False):
    compare, updates = parse(text)

    incorrect_updates = (
        update
        for update in updates
        if any(
            compare(update[idx], update[idx + 1]) == 1 for idx in range(len(update) - 1)
        )
    )
    result = sum(
        int(sorted(update, key=functools.cmp_to_key(compare))[len(update) // 2])
        for update in incorrect_updates
    )

    return result
