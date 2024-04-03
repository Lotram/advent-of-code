import hashlib
from itertools import count


def part_1(text, example: bool = False):
    word = text.strip()
    counter = count(0)
    result = ""
    while len(result) < 8:
        idx = next(counter)
        digest = hashlib.md5(f"{word}{idx}".encode()).hexdigest()
        if digest[:5] == "0" * 5:
            result = f"{result}{digest[5]}"

    return result


def part_2(text, example: bool = False):
    word = text.strip()
    counter = count(0)
    result: list[None | str] = [None] * 8
    while any(char is None for char in result):
        idx = next(counter)
        digest = hashlib.md5(f"{word}{idx}".encode()).hexdigest()

        if (
            digest[:5] == "0" * 5
            and 0 <= (pos := int(digest[5], 16)) < 8
            and result[pos] is None
        ):
            result[pos] = digest[6]

    return "".join(result)
