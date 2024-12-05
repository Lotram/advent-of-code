import cmath
from collections import defaultdict


def get_points(text):
    return [
        complex(col_idx, row_idx)
        for row_idx, line in enumerate(text.strip().splitlines())
        for col_idx, char in enumerate(line)
        if char == "#"
    ]


def get_key(number):
    return -cmath.phase(number.conjugate() * complex(0, 1))


def get_max_visible(points):
    vectors = {point: defaultdict(set) for point in points}
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            vector = points[j] - points[i]
            vectors[points[i]][get_key(vector)].add(vector)
            vectors[points[j]][get_key(-vector)].add(-vector)

    visible, point = max(
        ((visible, point) for point, visible in vectors.items()),
        key=lambda item: len(item[0]),
    )
    return visible, point


def part_1(text, example: bool = False):
    points = get_points(text)
    result, point = get_max_visible(points)
    print(point)
    return len(result)


def part_2(text, example: bool = False):
    points = get_points(text)

    vectors, point = get_max_visible(points)
    ordered = sorted(
        (idx, argument, vector, vector + point)
        for argument, _vectors in vectors.items()
        for idx, vector in enumerate(sorted(_vectors, key=abs))
    )

    res = ordered[199][-1]
    result = int(res.real * 100 + res.imag)
    return result
