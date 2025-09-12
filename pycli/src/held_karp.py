import math
from itertools import combinations


def held_karp_bitmask(distances, max_value=False):
    """
    Algorithm to solve Traveling Salesperson Problem (shortest hamiltonian cycle)
    """
    N = len(distances)
    func = max if max_value else min
    # memoization table, where keys are pairs (subset of nodes, node) and values are costs
    costs = {(1 << node, node): (distances[node][0], 0) for node in range(1, N)}

    # Iterate over subsets of increasing length
    for subset_size in range(2, N):
        for subset in combinations(range(1, N), subset_size):
            # Set bits for all nodes in subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            # Find the lowest cost to get to this subset
            for node in subset:
                prev = bits & ~(1 << node)
                res = []
                for m in subset:
                    if m == 0 or m == node:
                        continue
                    res.append((costs[(prev, m)][0] + distances[m][node], m))
                costs[(bits, node)] = func(res)

    # We're at the last node looking back to all other nodes to find the min / max path
    bits = (2**N - 1) - 1  # All nodes except the 0th
    res = []
    for node in range(1, N):
        res.append((costs[(bits, node)][0] + distances[node][0], node))
    opt, prev = func(res)

    # Backtrack to find full path
    path = []
    for i in range(N - 1):
        path.append(prev)
        new_bits = bits & ~(1 << prev)
        _, prev = costs[(bits, prev)]
        bits = new_bits

    # Add start node and reverse path
    path.append(0)
    path.reverse()

    return opt, path


def held_karp(distances, max_value=False, predecessors=None):
    N = len(distances)
    all_nodes = frozenset(range(1, N))
    func = max if max_value else min

    def preds_satisfied_in_subset(j, subset_visited):
        if not predecessors:
            return True
        # All predecessors of j are already visited
        return all(
            _pred in subset_visited or _pred == 0
            for _pred in predecessors.get(j, set())
        )

    def subset_respects_precedence(subset):
        if not predecessors:
            return True

        return all(
            all(
                _pred in subset or _pred == 0
                for _pred in predecessors.get(_node, set())
            )
            for _node in subset
        )

    # memoization table, where keys are pairs (frozenset of nodes, last node in path) and values are costs
    costs = {
        (frozenset([idx]), idx): (distances[0][idx], 0)
        for idx in all_nodes
        if preds_satisfied_in_subset(idx, set())
    }

    # Helper function to find the minimum cost to go through all nodes from subset and to end in node last_node
    def get_min_cost(subset, last_node):
        prev_subset = subset - {last_node}

        if not preds_satisfied_in_subset(last_node, prev_subset):
            return float("inf"), None

        min_cost, min_prev_node = func(
            (
                (costs[(prev_subset, _node)][0] + distances[_node][last_node], _node)
                for _node in prev_subset
                if (prev_subset, _node) in costs
            ),
            default=(math.inf, None),
        )
        return min_cost, min_prev_node

    # Main loop over all subset sizes
    for subset_size in range(2, N):
        for subset in map(frozenset, combinations(all_nodes, subset_size)):
            if not subset_respects_precedence(subset):
                continue
            costs.update(
                {(subset, node): get_min_cost(subset, node) for node in subset}
            )

    # Full set case (all nodes)
    full_set_cost, last_node = func(
        (costs[(all_nodes, node)][0] + distances[node][0], node)
        for node in all_nodes
        if (all_nodes, node) in costs
    )

    node = last_node
    path = []
    subset = all_nodes
    for _ in range(N - 1):
        _, next_node = costs[(subset, node)]
        path.append(node)
        subset -= {node}
        node = next_node

    # Add the start node and reverse path to get the correct order
    path.append(0)
    path.reverse()
    return full_set_cost, path


def shortest_hamiltionan_path(distances, max_value=False):
    """
    Similar to TSP, but without the need to return to the start
    """
    distances = [[0] * (len(distances) + 1), *[[0, *row] for row in distances]]
    cost, path = held_karp_bitmask(distances, max_value)
    return cost, [idx - 1 for idx in path[1:]]
