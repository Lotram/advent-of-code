from functools import cache
from itertools import batched
from operator import methodcaller

from sympy import proper_divisors


def part_1(text, example: bool = False):
    result = 0
    for start, end in map(methodcaller("split", "-"), text.split(",")):
        for value in range(int(start), int(end) + 1):
            str_value = str(value)
            if len(str_value) % 2 == 1:
                continue
            half_len = len(str_value) // 2
            if str_value[:half_len] == str_value[half_len:]:
                result += value

    return result


@cache
def get_divisors(length):
    return proper_divisors(length)


def all_equal(iterable):
    iterator = iter(iterable)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)


def find_invalids(value):
    length = len(value)
    return any(all_equal(batched(value, divisor)) for divisor in get_divisors(length))


# TODO: be smarter than that
# we can produce the invalid ids without having to iterate on all values.
def part_2(text, example: bool = False):
    result = 0
    for start, end in map(methodcaller("split", "-"), text.split(",")):
        for value in range(int(start), int(end) + 1):
            if find_invalids(str(value)):
                result += value

    return result
