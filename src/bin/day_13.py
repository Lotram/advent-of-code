def is_similar(left, right):
    return len(get_diffs(left, right)) <= 1


def get_diffs(left, right):
    return [idx for idx in range(len(left)) if left[idx] != right[idx]]


def find_reflexion(rows):
    rows = list(map(tuple, rows))
    candidates = [
        idx for idx in range(1, len(rows)) if is_similar(rows[idx], rows[idx - 1])
    ]
    for candidate in candidates:
        can_change = True
        is_mirror = True
        left, right = rows[:candidate][::-1], rows[candidate:]
        for idx, (l, r) in enumerate(zip(left, right)):
            if l == r:
                continue
            elif can_change and is_similar(l, r):
                can_change = False

            else:
                is_mirror = False

        if is_mirror and not can_change:
            return candidate


def find_reflexions(pattern):
    rows = pattern.split("\n")
    idx = find_reflexion(rows)
    if idx is not None:
        return 100 * idx

    columns = list(zip(*rows))
    return find_reflexion(columns)


def part_1(text):
    result = 0
    for pattern in text.strip().split("\n\n"):
        result += find_reflexions(pattern)
    print(result)


def part_2(text):
    result = 0
    for pattern in text.strip().split("\n\n"):
        result += find_reflexions(pattern)
    print(result)
