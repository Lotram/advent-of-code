import string


def is_pair(a, b):
    return abs(ord(a) - ord(b)) == 32  # ord("a") - ord("A")


def solution(text, skipped_char=None):
    line = list(text.strip())[::-1]
    consumed = []
    while line:
        item = line.pop()
        if item.lower() == skipped_char:
            continue
        if consumed and is_pair(item, consumed[-1]):
            consumed.pop()
        else:
            consumed.append(item)

    result = len(consumed)
    return result


def part_1(text, example: bool = False):
    return solution(text)


def part_2(text, example: bool = False):
    return min(solution(text, char) for char in string.ascii_lowercase)
