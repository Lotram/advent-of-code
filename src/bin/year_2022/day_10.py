def f(cycle):
    return (cycle - 20) // 40


def get_strength(cycle, inc, value):
    if (impulse := f(cycle + inc)) > f(cycle):
        return value * (20 + impulse * 40)
    return 0


def parse(lines):
    value = 1
    cycle = 0
    result = 0
    for line in lines:
        op, *val = line.split()
        inc = 1 if op == "noop" else 2
        result += get_strength(cycle, inc, value)
        cycle += inc

        if op == "addx":
            value += int(val[0])

    return result


def part_1(text):
    lines = text.strip().split("\n")
    return parse(lines)


def get_pixel(cycle, sprite):
    return "#" if abs(cycle % 40 - sprite) <= 1 else "."


def parse_2(lines):
    sprite = 1
    cycle = 0
    rows = []
    current_row = []
    for line in lines:
        op, *val = line.split()

        inc = 1 if op == "noop" else 2
        for _ in range(inc):
            current_row.append(get_pixel(cycle, sprite))
            cycle += 1
            if cycle % 40 == 0:
                rows.append(current_row)
                current_row = []

        if op == "addx":
            sprite += int(val[0])

    if current_row:
        rows.append(current_row)
    return rows


def display(rows):
    for row in rows:
        print("".join(row))


def part_2(text):
    lines = text.strip().split("\n")
    display(parse_2(lines))
