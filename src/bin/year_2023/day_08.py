import math
import re
from itertools import cycle, product

PATTERN = re.compile(r"(?P<position>\w{3}) = \((?P<left>\w{3}), (?P<right>\w{3})\)")


def part_1(lines):
    result = None
    print(result)


def find_cycle(start_node, nodes, directions):
    node_cycle = {(start_node, directions[0]): 0}
    current_node = start_node
    direction_iter = cycle(enumerate(directions))
    while True:
        dir_idx, direction = next(direction_iter)
        next_node = nodes[current_node][0 if direction == "L" else 1]
        if (next_node, dir_idx) in node_cycle:
            return list(node_cycle)
        else:
            node_cycle[(next_node, dir_idx)] = len(node_cycle)

        current_node = next_node


def get_ending_node_positions(node_cycle):
    return {idx for idx, node in enumerate(node_cycle) if node[0][-1] == "Z"}


def part_2(lines):
    lines = lines.split("\n")
    directions = lines[0]
    nodes = {}
    for line in lines[2:]:
        match = PATTERN.match(line)
        if not match:
            continue

        nodes[match.group("position")] = (
            match.group("left"),
            match.group("right"),
        )

    start_nodes = [node for node in nodes if node[2] == "A"]
    end_positions = []
    node_cycles = []
    for start_node in start_nodes:
        node_cycle = find_cycle(start_node, nodes, directions)
        node_cycles.append(node_cycle)
        end_positions.append(get_ending_node_positions(node_cycle))

    # result = 21_003_205_388_413
    return min(math.lcm(*end_pos) for end_pos in product(*end_positions))
