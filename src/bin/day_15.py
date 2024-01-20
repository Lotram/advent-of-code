import math
import re
from functools import partial

import numpy as np

pattern = re.compile(r"[-\d]+")


def get_tuples(length, total):
    if length == 1:
        yield (total,)
        return

    yield from (
        (i,) + t for i in range(total + 1) for t in get_tuples(length - 1, total - i)
    )


def part_1(text):
    lines = text.strip().split("\n")
    values = []
    for line in lines:
        *_values, _ = map(int, pattern.findall(line))
        values.append(_values)
    max_ = partial(max, 0)
    tuple_it = get_tuples(len(lines), 100)
    vectors = (map(max_, np.matmul(tup, values)) for tup in tuple_it)
    result = max(math.prod(vector) for vector in vectors)
    return result


def part_2(text):
    lines = text.strip().split("\n")
    values = []
    for line in lines:
        _values = list(map(int, pattern.findall(line)))
        values.append(_values)
    max_ = partial(max, 0)
    tuple_it = get_tuples(len(lines), 100)
    vectors = (list(map(max_, np.matmul(tup, values))) for tup in tuple_it)
    result = max(math.prod(vector[:-1]) for vector in vectors if vector[-1] == 500)
    return result
