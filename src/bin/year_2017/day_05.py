def part_1(text, example: bool = False):
    jumps = list(map(int, text.strip().split("\n")))
    cursor = 0
    result = 0
    while 0 <= cursor < len(jumps):
        jump = jumps[cursor]
        jumps[cursor] += 1
        cursor += jump
        result += 1

    return result


def part_2(text, example: bool = False):
    jumps = list(map(int, text.strip().split("\n")))
    cursor = 0
    result = 0
    while 0 <= cursor < len(jumps):
        jump = jumps[cursor]
        jumps[cursor] += 1 if jump < 3 else -1
        cursor += jump
        result += 1

    return result
