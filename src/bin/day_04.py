import hashlib


def solution(key, trailing_zeros):
    idx = 0
    while True:
        data = key + str(idx).encode()
        if hashlib.md5(data).hexdigest()[:trailing_zeros] == "0" * trailing_zeros:
            break
        idx += 1

    return idx


def part_1(text):
    key = text.strip().encode()
    return solution(key, 5)


def part_2(text):
    key = text.strip().encode()
    return solution(key, 6)
