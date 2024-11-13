import networkx
from pycli.src.grid import EAST, NORTH, SOUTH, WEST, Vector


DIRECTIONS = {"N": NORTH, "W": WEST, "E": EAST, "S": SOUTH}


def get_graph(text):
    graph = networkx.DiGraph()
    current_positions = {Vector(0, 0)}
    stack = []
    starts, ends = {Vector(0, 0)}, set()
    for char in text:
        match char:
            case "^" | "$":
                pass
            case "N" | "E" | "W" | "S":
                direction = DIRECTIONS[char]
                graph.add_edges_from(
                    (position, position + direction) for position in current_positions
                )
                current_positions = {
                    position + direction for position in current_positions
                }

            case "(":
                stack.append((starts, ends))
                starts, ends = current_positions, set()

            case "|":
                ends |= current_positions
                current_positions = starts

            case ")":
                current_positions |= ends
                starts, ends = stack.pop()

    return graph


def part_1(text, example: bool = False):
    graph = get_graph(text)

    result = max(networkx.algorithms.shortest_path_length(graph, Vector(0, 0)).values())

    return result


def part_2(text, example: bool = False):
    graph = get_graph(text)

    result = sum(
        1
        for length in networkx.algorithms.shortest_path_length(
            graph, Vector(0, 0)
        ).values()
        if length >= 1_000
    )

    return result
