import re
from itertools import chain


pattern = re.compile(r"\.|#")


def parse_initial_state(line) -> frozenset[int]:
    chars = line.removeprefix("initial state: ")
    assert all(char in {".", "#"} for char in chars)
    return frozenset(idx for idx, char in enumerate(chars) if char == "#")


def parse_masks(masks):
    return {
        tuple(map("#".__eq__, mask)): result == "#"
        for *mask, result in map(pattern.findall, masks)
    }


def next_generation(
    state: frozenset[int],
    masks: dict[tuple[bool, bool, bool, bool, bool], bool],
):
    return frozenset(
        idx
        for idx in set(chain.from_iterable(range(idx - 2, idx + 3) for idx in state))
        if masks.get(tuple(map(state.__contains__, range(idx - 2, idx + 3))), False)
    )


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    state = parse_initial_state(lines[0])
    masks = parse_masks(lines[2:])
    for _ in range(20):
        state = next_generation(state, masks)
    return sum(state)


def center_state(state):
    min_val = min(state)
    return min_val, frozenset(val - min_val for val in state)


def part_2(text, example: bool = False):
    loops = 50_000_000_000
    lines = text.strip().split("\n")
    state = parse_initial_state(lines[0])
    masks = parse_masks(lines[2:])
    states = {state: (0, 0)}
    for generation in range(loops):
        state = next_generation(state, masks)
        min_val, centered_state = center_state(state)
        if centered_state in states:
            previous_gen, previous_min_val = states[centered_state]
            assert generation - min_val == previous_gen - previous_min_val
            result = sum(centered_state) + (
                loops - previous_gen + previous_min_val - 1
            ) * len(centered_state)
            break
        states[centered_state] = (generation, min_val)
    else:
        raise RuntimeError("no loop found")
    return result
