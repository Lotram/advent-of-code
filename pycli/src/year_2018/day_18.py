import numpy as np
from pycli.src.grid import Grid


"""
* An *open* acre will become filled with *trees* if *three or more* adjacent acres contained trees. Otherwise, nothing happens.
* An acre filled with *trees* will become a *lumberyard* if *three or more* adjacent acres were lumberyards. Otherwise, nothing happens.
* An acre containing a *lumberyard* will remain a *lumberyard* if it was adjacent to *at least one other lumberyard and at least one acre containing trees*. Otherwise, it becomes *open*.
"""

next_states = {".": "|", "|": "#", "#": "."}


def get_new_state(value, neighbours):
    match value:
        case "." | "|":
            next_state = next_states[value]
            return (
                next_state
                if sum(neighbour == next_state for _, neighbour in neighbours) >= 3
                else value
            )
        case "#":
            return (
                "#" if {neighbour for _, neighbour in neighbours} >= {"#", "|"} else "."
            )


def part_1(text, example: bool = False):
    grid = Grid.from_text(text, diag=True)
    for _ in range(10):
        new_arr = grid.arr.copy()
        for position, value in grid.flat_iter():
            new_arr[position] = get_new_state(value, grid.neighbours(position))
        grid.arr = new_arr

    result = len(grid.find_all("#")) * len(grid.find_all("|"))
    return result


def get_hash(grid):
    return hash("".join(val for _, val in grid.flat_iter()))


def get_result(grid):
    return len(grid.find_all("#")) * len(grid.find_all("|"))


def part_2(text, example: bool = False):
    grid = Grid.from_text(text, diag=True)
    states = {}
    results = []
    for idx in range(1_000_000_000):
        grid_hash = get_hash(grid)
        if loop_start := states.get(grid_hash):
            break
        states[grid_hash] = idx
        results.append(get_result(grid))
        new_arr = grid.arr.copy()
        for position, value in grid.flat_iter():
            new_arr[position] = get_new_state(value, grid.neighbours(position))

        grid.arr = new_arr

    else:
        raise ValueError("reached end of loop")

    remainder = (1_000_000_000 - loop_start) % (idx - loop_start)
    result = results[loop_start + remainder]
    return result
