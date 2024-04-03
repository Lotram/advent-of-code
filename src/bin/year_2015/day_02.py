def part_1(text):
    lines = text.strip().split("\n")
    result = 0
    for line in lines:
        l, w, h = map(int, line.split("x"))
        lw, lh, wh = l * w, l * h, w * h
        result += 2 * (lw + lh + wh) + min([lw, lh, wh])

    return result


def part_2(text):
    lines = text.strip().split("\n")
    result = 0
    for line in lines:
        l, w, h = sorted(map(int, line.split("x")))

        result += 2 * (l + w) + l * w * h

    return result
