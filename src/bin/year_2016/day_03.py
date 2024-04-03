from itertools import batched


def part_1(text):
    lines = text.strip().split("\n")
    result = 0
    for line in lines:
        values = sorted(map(int, line.split()))
        if values[2] < values[0] + values[1]:
            result += 1
    return result


def part_2(text):
    lines = text.strip().split("\n")
    result = 0
    for batch in batched(lines, 3):
        triangles = []
        for line in batch:
            values = list(map(int, line.split()))
            triangles.append(values)

        for values in map(sorted, zip(*triangles)):
            if values[2] < values[0] + values[1]:
                result += 1
    return result
