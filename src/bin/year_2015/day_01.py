def part_1(text):
    line = text.strip().split("\n")[0]
    result = line.count("(") - line.count(")")
    return result


def part_2(text):
    line = text.strip().split("\n")[0]
    floor = 0
    for idx, char in enumerate(line, start=1):
        floor += 1 if char == "(" else -1
        if floor < 0:
            break
    return idx
