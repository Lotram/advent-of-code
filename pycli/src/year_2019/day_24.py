from collections import defaultdict
from collections.abc import Iterator
from itertools import batched, chain

from pycli.src.grid import Grid


def next_state(grid: Grid):
    new_arr = grid.arr.copy()
    for position, value in grid.flat_iter():
        adjacent_bugs = sum(value for _, value in grid.neighbours(position))
        if (value and adjacent_bugs != 1) or (not value and adjacent_bugs in {1, 2}):
            new_arr[position] = not value

    grid.arr = new_arr


def get_neighbours(i: int):
    if i % 5:
        yield i - 1

    if i % 5 < 4:
        yield i + 1

    if i - 5 >= 0:
        yield i - 5

    if i + 5 < 25:
        yield i + 5


def get_score(grid):
    return sum(value * 2**i for i, (_, value) in enumerate(grid.flat_iter()))


def part_1(text, example: bool = False):
    grid = Grid.from_text(text, truthy_value="#")
    scores = set()
    score = get_score(grid)
    while score not in scores:
        scores.add(score)
        next_state(grid)
        score = get_score(grid)
    return score


def get_neighbours_2(i: int, layer_idx: int) -> Iterator[tuple[int, int]]:
    if i == 12:
        return
    # Left
    if i == 13:
        yield from ((_val, layer_idx + 1) for _val in range(4, 25, 5))

    elif i % 5 == 0:
        yield (11, layer_idx - 1)

    else:
        yield (i - 1, layer_idx)

    # Right
    if i == 11:
        yield from ((_val, layer_idx + 1) for _val in range(0, 25, 5))

    elif i % 5 == 4:
        yield (13, layer_idx - 1)

    else:
        yield (i + 1, layer_idx)

    # UP
    if i == 17:
        yield from ((_val, layer_idx + 1) for _val in range(20, 25))
    elif i <= 4:
        yield (7, layer_idx - 1)
    else:
        yield (i - 5, layer_idx)

    # DOWN
    if i == 7:
        yield from ((_val, layer_idx + 1) for _val in range(5))
    elif i >= 20:
        yield (17, layer_idx - 1)
    else:
        yield (i + 5, layer_idx)


def next_state_2(all_values, layer_idx):
    return tuple(
        value ^ (adjacent_bugs != 1 if value else adjacent_bugs in {1, 2})
        for value, adjacent_bugs in (
            (
                value,
                sum(
                    all_values[_layer_idx][neighbour]
                    for neighbour, _layer_idx in get_neighbours_2(i, layer_idx)
                ),
            )
            for i, value in enumerate(all_values[layer_idx])
        )
    )


def layer_str(layer):
    return "\n".join(
        [
            "".join(line)
            for line in batched(
                [
                    ("#" if char else ".") if idx != 12 else "?"
                    for idx, char in enumerate(layer)
                ],
                5,
            )
        ]
    )


def part_2(text, example: bool = False):
    layers = defaultdict(lambda: (False,) * 25)
    layers[0] = tuple(char == "#" for line in text.splitlines() for char in line)
    min_layer = max_layer = 0
    for _ in range(200):
        new_values: defaultdict[int, tuple[bool, ...]] = defaultdict(
            lambda: (False,) * 25
        )
        min_layer = min(layers)
        max_layer = max(layers)
        for layer_idx in range(min_layer - 1, max_layer + 2):
            new_state = next_state_2(layers, layer_idx)
            if any(new_state):
                new_values[layer_idx] = new_state

        layers = new_values
        min_layer = min(layers)

    return sum(chain.from_iterable(layers.values()))
