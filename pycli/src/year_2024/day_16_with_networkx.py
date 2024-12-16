import networkx
from pycli.src.grid import DIRECTIONS, EAST, Grid, Vector


def parse(text) -> tuple[networkx.Graph, Vector, Vector]:
    graph = networkx.DiGraph()
    grid = Grid.from_text(text)
    start = grid.find("S")
    end = grid.find("E")
    maze = {position for position, value in grid.flat_iter() if value != "#"}
    for position in maze:
        for direction in DIRECTIONS:
            graph.add_edge(
                (position, direction), (position, direction.rotate(1)), weight=1000
            )
            graph.add_edge(
                (position, direction), (position, direction.rotate(-1)), weight=1000
            )
            if position + direction in maze:
                graph.add_edge(
                    (position, direction), (position + direction, direction), weight=1
                )

    return graph, start, end


def part_1(text, example: bool = False):
    graph, start, end = parse(text)
    ends = [(end, direction) for direction in DIRECTIONS]
    result = min(
        networkx.shortest_path_length(graph, (start, EAST), end, weight="weight")
        for end in ends
    )
    return result


def part_2(text, example: bool = False):
    graph, start, end = parse(text)
    ends = [(end, direction) for direction in DIRECTIONS]
    shortest_path_length = min(
        networkx.shortest_path_length(graph, (start, EAST), end, weight="weight")
        for end in ends
    )
    ends = [
        end
        for end in ends
        if networkx.shortest_path_length(graph, (start, EAST), end, weight="weight")
        == shortest_path_length
    ]

    result = len(
        {
            node[0]
            for end in ends
            for path in networkx.all_shortest_paths(
                graph, (start, EAST), end, weight="weight"
            )
            for node in path
        }
    )

    return result
