import math
import random
from typing import Generic, TypeVar

from pydantic import BaseModel


NodeType = TypeVar("NodeType", str, int)


class Edge(BaseModel, Generic[NodeType]):
    src: NodeType
    dest: NodeType

    def __repr__(self) -> str:
        return f"Edge({self.src} <--> {self.dest})"


# A class to represent a subset for union-find
class Subset(BaseModel, Generic[NodeType]):
    parent: NodeType
    rank: int
    size: int


class DisjointSet(BaseModel, Generic[NodeType]):
    elements: dict[NodeType, Subset[NodeType]]
    roots: set[NodeType]

    @classmethod
    def from_sequence(cls, elements):
        return cls(
            elements={
                element: Subset(parent=element, rank=0, size=1) for element in elements
            },
            roots=set(elements),
        )

    def find(self, element: NodeType) -> NodeType:
        subset = self.elements[element]
        if subset.parent != element:
            subset.parent = self.find(subset.parent)

        return subset.parent

    def union(self, x: NodeType, y: NodeType) -> None:
        xroot = self.find(x)
        yroot = self.find(y)

        x_subset = self.elements[xroot]
        y_subset = self.elements[yroot]
        # Attach smaller rank tree under root of high
        # rank tree (union by Rank)
        if x_subset.rank < y_subset.rank:
            x_subset.parent = yroot
            y_subset.size += x_subset.size
            self.roots.remove(xroot)

        else:
            y_subset.parent = xroot
            x_subset.size += y_subset.size
            self.roots.remove(yroot)

            # If ranks are same, then make one as root and
            # increment its rank by one
            x_subset.rank += x_subset.rank == y_subset.rank

    def __repr__(self) -> str:
        return f"DisjointSet(sets={len(self.roots)})"


class DisjointSetGraph(BaseModel, Generic[NodeType]):
    disjoint_set: DisjointSet[NodeType]
    edges: list[Edge[NodeType]]

    def contract(self, val: int) -> None:
        # Keep contracting vertices until there are
        # val vertices.
        edges = random.sample(self.edges, k=len(self.edges))
        while len(self.disjoint_set.roots) > val:
            edge = edges.pop()

            subset1 = self.disjoint_set.find(edge.src)
            subset2 = self.disjoint_set.find(edge.dest)

            # If the two ends of the edge belong to same subset,
            # then no point considering this edge
            if subset1 != subset2:
                self.disjoint_set.union(subset1, subset2)

        self.edges = [
            edge
            for edge in edges
            if self.disjoint_set.find(edge.src) != self.disjoint_set.find(edge.dest)
        ]

    def min_cut(self) -> int:
        self.contract(2)
        return len(self.edges)

    def __repr__(self) -> str:
        return f"DisjointSetGraph(vertices={len(self.disjoint_set.roots)}, edges={len(self.edges)})"


# a class to represent a connected, undirected
# and unweighted graph as a collection of edges.
class Graph(BaseModel, Generic[NodeType]):
    vertices: set[NodeType]
    edges: list[Edge[NodeType]]

    # TODO: fast is not faster. Either remove the deepcopy, or find expensive operations
    def min_cut(self, fast=False):
        disjoint_set = DisjointSet.from_sequence(self.vertices)
        ds_graph = DisjointSetGraph(disjoint_set=disjoint_set, edges=self.edges.copy())

        if fast:
            return _fast_min_cut(ds_graph), ds_graph

        return ds_graph.min_cut(), ds_graph

    def __repr__(self) -> str:
        return f"Graph(vertices={len(self.vertices)}, edges={len(self.edges)})"


def _fast_min_cut(ds_graph: DisjointSetGraph):
    ds_graph = ds_graph.model_copy(deep=True)
    vertex_count = len(ds_graph.disjoint_set.roots)
    if vertex_count <= 6:
        return ds_graph.min_cut()
    else:
        threshold = math.ceil(1 + vertex_count / math.sqrt(2))
        copied = ds_graph.model_copy(deep=True)
        ds_graph.contract(threshold)
        copied.contract(threshold)

        return min(_fast_min_cut(ds_graph), _fast_min_cut(copied))
