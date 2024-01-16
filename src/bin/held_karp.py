from itertools import combinations


def held_karp_bitmask(distances):
    n = len(distances)
    # memoization table, where keys are pairs (subset of nodes, node) and values are costs
    costs = {(1 << node, node): (distances[node][0], 0) for node in range(1, n)}

    # Iterate over subsets of increasing length
    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
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
                costs[(bits, node)] = min(res)

    # We're at the last node looking back to all other nodes to find the minimum path
    bits = (2**n - 1) - 1  # All nodes except the 0th
    res = []
    for node in range(1, n):
        res.append((costs[(bits, node)][0] + distances[node][0], node))
    opt, prev = min(res)

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(prev)
        new_bits = bits & ~(1 << prev)
        _, prev = costs[(bits, prev)]
        bits = new_bits

    # Add start node and reverse path
    path.append(0)
    path.reverse()

    return opt, path


def held_karp(distances):
    n = len(distances)
    all_nodes = frozenset(range(1, n))
    # memoization table, where keys are pairs (frozenset of nodes, last node in path) and values are costs
    costs = {(frozenset([idx]), idx): (distances[0][idx], 0) for idx in all_nodes}

    # Helper function to find the minimum cost to reach a subset ending in node node
    def get_min_cost(subset, last_node):
        prev_subset = subset - {last_node}
        min_cost, min_prev_node = min(
            (costs[(prev_subset, _node)][0] + distances[_node][last_node], _node)
            for _node in prev_subset
        )
        return min_cost, min_prev_node

    # Main loop over all subset sizes
    for r in range(2, n):
        for subset in map(frozenset, combinations(all_nodes, r)):
            costs.update(
                {(subset, node): get_min_cost(subset, node) for node in subset}
            )

    # Full set case (all nodes)
    full_set_cost, last_node = min(
        (costs[(all_nodes, node)][0] + distances[node][0], node) for node in all_nodes
    )

    node = last_node
    path = []
    subset = all_nodes
    for _ in range(n - 1):
        _, next_node = costs[(subset, node)]
        path.append(node)
        subset -= {node}
        node = next_node

    # Add the start node and reverse path to get the correct order
    path.append(0)
    path.reverse()
    return full_set_cost, path
