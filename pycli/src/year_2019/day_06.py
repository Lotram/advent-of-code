import networkx as nx


def build_tree(text):
    tree = nx.DiGraph([line.split(")") for line in text.strip().splitlines()])
    assert nx.is_arborescence(tree)
    return tree


def part_1(text, example: bool = False):
    tree = build_tree(text)
    ancestors = {"COM": 0}
    for node in tree:
        values = {}
        current = node
        while current not in ancestors:
            values[current] = 0
            values = {_node: value + 1 for _node, value in values.items()}
            current = next(tree.predecessors(current), None)
        values = {_node: value + ancestors[current] for _node, value in values.items()}
        ancestors.update(values)

    result = sum(ancestors.values())
    return result


def part_2(text, example: bool = False):
    tree = build_tree(text)
    result = nx.shortest_path(
        tree.to_undirected(),
        next(tree.predecessors("YOU")),
        next(tree.predecessors("SAN")),
    )
    return len(result) - 1
