from itertools import groupby


def get_next(password):
    password = password.copy()
    idx = len(password) - 1
    while True:
        if password[idx] != "z":
            increment_by = 2 if password[idx] in "hnk" else 1
            password[idx] = chr(ord(password[idx]) + increment_by)
            return password
        password[idx] = "a"
        idx -= 1


def pair_count(chars):
    double_count = 0
    for _, group in groupby(chars):
        double_count += len(list(group)) // 2

    return double_count


def has_straight(chars):
    for idx in range(2, len(chars)):
        if ord(chars[idx]) == ord(chars[idx - 1]) + 1 == ord(chars[idx - 2]) + 2:
            return True

    return False


def next_without_forbidden(password):
    for idx in range(3):
        if password[idx] in "iol":
            for k in range(idx + 1, len(password)):
                password[k] = "a"
            password[idx] = chr(ord(password[idx]) + 1)
    return password


def is_compliant(chars):
    return has_straight(chars) and pair_count(chars) >= 2


def solution_1(password):
    password = password.copy()
    while True:
        password = get_next(password)

        if is_compliant(password):
            return password


def solution_2(password):
    password = password.copy()
    password = get_next(password)
    if pair_count(password[:3]) >= 1:
        raise NotImplementedError("edge case to handle")

    if password[3] > "x":
        password[3] = "a"

    ord_ = ord(password[3])
    password[4] = chr(ord_)
    password[5] = chr(ord_ + 1)
    password[6] = chr(ord_ + 2)
    password[7] = chr(ord_ + 2)
    return password


def part_1(text, example: bool = False):
    password = list(text.strip())
    password = next_without_forbidden(password)
    password = "".join(solution_2(password))
    return password


def part_2(text, example: bool = False):
    password = list(text.strip())
    password = next_without_forbidden(password)
    password = solution_2(password)
    password = "".join(solution_2(password))
    return password
