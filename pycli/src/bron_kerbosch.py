r"""
Algorithm to list all maximal cliques in a graph

see https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm

"""


class BronKerbosh:
    def __init__(self, graph):
        self.graph = graph
        self.outputs = []

    def run(self, version=1):
        bron_kerbosch = self.bron_kerbosch_v1 if version == 1 else self.bron_kerbosch_v2
        bron_kerbosch(set(), set(self.graph), set())
        return self.outputs

    def get_neighbours(self, node):
        return set(self.graph[node])

    def bron_kerbosch_v1(self, R, P, X):
        if not (P or X):
            self.outputs.append(R)
        for node in list(P):
            neighbours = self.get_neighbours(node)
            self.bron_kerbosch_v1(R | {node}, P & neighbours, X & neighbours)
            P -= {node}
            X |= {node}

    def bron_kerbosch_v2(self, R, P, X):
        if not (P or X):
            self.outputs.append(R)
            return

        pivot = max(
            (node for node in P | X), key=lambda node: len(self.get_neighbours(node))
        )
        for node in list(P - self.get_neighbours(pivot)):
            neighbours = self.get_neighbours(node)
            self.bron_kerbosch_v2(R | {node}, P & neighbours, X & neighbours)
            P -= {node}
            X |= {node}
