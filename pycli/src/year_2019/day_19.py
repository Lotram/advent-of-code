import concurrent.futures
from fractions import Fraction
from functools import partial
from itertools import count, product

from pycli.src.year_2019.intcode import ListIntCodeComputer


def _init_worker(shared_text: str) -> None:
    """Initializer run once in each worker process to set global state."""
    global _GLOBAL_TEXT
    _GLOBAL_TEXT = shared_text


def _run_computer(text, coords):
    x, y = coords
    computer = ListIntCodeComputer.from_text(text)
    computer.put(x)
    computer.put(y)
    computer.run()
    return int(computer.get())


def part_1(text, example: bool = False):
    result = 0
    SIZE = 50
    inputs = list(product(range(SIZE), repeat=2))

    with (
        concurrent.futures.ProcessPoolExecutor(
            # initializer=_init_worker, initargs=(text,)
        ) as executor
    ):
        result = sum(executor.map(partial(_run_computer, text), inputs))

    return result


def find_points(grid, size):
    xs = []
    min_ys = []
    max_ys = []
    for x in range(6, size):
        xs.append(x)
        min_y = next(y for y in count() if grid[y, x] == "#")
        max_y = next(y for y in count(min_y + 1) if grid[y, x] == ".") - 1
        min_ys.append(min_y)
        max_ys.append(max_y)

    return xs, min_ys, max_ys


def sign(value):
    return 1 if value else -1


def find_y(run_computer, x, y, is_min):
    first_value = run_computer((x, y))
    value = first_value
    while value == first_value:
        y += sign(is_min ^ value)
        value = run_computer((x, y))

    y += sign(is_min) * first_value
    return y


def find_coef(run_computer, is_min):
    prev_coef = int(not is_min)
    x = 10
    if is_min:
        prev_coef = 0
    else:
        min_y = find_y(run_computer, x, y=0, is_min=True)
        max_y = find_y(run_computer, x, y=min_y + 1, is_min=True)
        prev_coef = max_y / x

    for x in [30, 50, 100, 1000, 10_000, 100_000]:
        approx_y = int(prev_coef * x)
        y = find_y(run_computer, x, approx_y, is_min)
        prev_coef = y / x
    return Fraction(prev_coef).limit_denominator(
        max_denominator=1000
    )  # assume the coefficient is a fraction with small integers


def part_2(text, example: bool = False):
    result = 0
    run_computer = partial(_run_computer, text)

    min_coef = find_coef(run_computer, is_min=True)  # actual value: 3/4
    max_coef = find_coef(run_computer, is_min=False)  # actual value: 12/13

    # equations = [
    #     y1 - min_coef * x2,
    #     y2 - max_coef * x1,
    #     y2 - y1 - 99,
    #     x2 - x1 - 99,
    # ]

    x1 = 99 * (min_coef + 1) / (max_coef - min_coef)

    # solution is magically an int, luck ?
    y1 = min_coef * (x1 + 99)

    result = int(x1 * 10_000 + y1)

    return result
