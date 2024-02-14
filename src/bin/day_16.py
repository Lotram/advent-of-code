from itertools import batched


def binary(int, length):
    return f"{int:b}".zfill(length)


def checksum(data):
    while len(data) % 2 == 0:
        data = "".join(str(int(i == j)) for i, j in batched(data, 2))
    return data


def _process(a):
    b = binary(int(a[::-1], 2) ^ int("1" * len(a), 2), len(a))
    return f"{a}0{b}"


def process(data, length):
    while len(data) < length:
        data = _process(data)
    return data[:length]


def part_1(text):
    data = text.strip()
    length = 20 if data == "10000" else 272
    data = process(data, length)
    result = checksum(data)
    return result


def part_2(text):
    data = text.strip()
    length = 20 if data == "10000" else 35651584
    data = process(data, length)
    result = checksum(data)
    return result
