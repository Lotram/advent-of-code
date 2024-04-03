from functools import cache
from itertools import count, cycle, dropwhile

from sympy import divisors


@cache
def pentagon(i):
    return i * (3 * i - 1) // 2


# https://fr.wikipedia.org/wiki/Fonction_somme_des_diviseurs
@cache
def sigma(n: int) -> int:
    if n == 1:
        return 1
    result = 0
    for it in [count(1), count(-1, -1)]:
        sign_it = cycle([1, -1])
        while True:
            i = next(it)
            pent = pentagon(i)
            if pent > n:
                break

            result += next(sign_it) * f(n - pent, n)
    return result


def f(k, n) -> int:
    if k > 0:
        return sigma(k)
    elif k == 0:
        return n
    else:
        return 0


def part_1_recursive(text):
    value = int(text.strip()) // 10
    result = 0
    incr = 1
    while sigma(result) < value:
        result += incr

    return result


def part_1(text, example: bool = False):
    value = int(text.strip())
    result = 1
    while sum(divisor for divisor in divisors(result, generator=True)) * 10 < value:
        result += 1

    return result


def part_2(text, example: bool = False):
    value = int(text.strip())
    result = 1
    while (
        sum(
            divisor
            for divisor in dropwhile(lambda d: result // d > 50, divisors(result))
        )
        * 11
        < value
    ):
        result += 1

    return result
