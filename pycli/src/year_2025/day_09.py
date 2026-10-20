from collections import defaultdict
from itertools import combinations, pairwise

from pycli.src.grid import Vector2D


def part_1(text, example: bool = False):
    vectors = [Vector2D(*map(int, line.split(","))) for line in text.splitlines()]
    result = float("-inf")

    for v1, v2 in combinations(vectors, 2):
        rectangle = v2 - v1
        area = (abs(rectangle.x) + 1) * (abs(rectangle.y) + 1)
        result = max(result, area)

    return result


class OrthogonalPolygon:
    def __init__(self, vertices: list[Vector2D]):
        self.vertices = vertices
        self.vertex_set = set(vertices)
        self.vertical_edges: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.horizontal_edges: dict[int, list[tuple[int, int]]] = defaultdict(list)

        for (ax, ay), (bx, by) in pairwise([*vertices, vertices[0]]):
            if ay == by:
                self.horizontal_edges[ay].append((min(ax, bx), max(ax, bx)))
            else:
                self.vertical_edges[ax].append((min(ay, by), max(ay, by)))

    def point_on_boundary(self, point: Vector2D) -> bool:
        return any(
            x_min <= point.x <= x_max
            for x_min, x_max in self.horizontal_edges.get(point.y, [])
        ) or any(
            y_min <= point.y <= y_max
            for y_min, y_max in self.vertical_edges.get(point.x, [])
        )

    def point_inside(self, point: Vector2D) -> bool:
        # https://wrfranklin.org/Research/Short_Notes/pnpoly.html
        if self.point_on_boundary(point):
            return True

        crossings = sum(
            1
            for vert_x, y_ranges in self.vertical_edges.items()
            if point.x < vert_x
            for y_min, y_max in y_ranges
            if y_min <= point.y < y_max
        )
        return crossings % 2 == 1

    def horizontal_edge_crosses(self, x1: int, x2: int, y: int) -> bool:
        return any(
            y_min < y < y_max
            for vert_x, y_ranges in self.vertical_edges.items()
            if x1 < vert_x < x2
            for y_min, y_max in y_ranges
        )

    def vertical_edge_crosses(self, x: int, y1: int, y2: int) -> bool:
        return any(
            x_min < x < x_max
            for horiz_y, x_ranges in self.horizontal_edges.items()
            if y1 < horiz_y < y2
            for x_min, x_max in x_ranges
        )

    def rectangle_inside(self, corner1: Vector2D, corner2: Vector2D) -> bool:
        min_x, max_x = min(corner1.x, corner2.x), max(corner1.x, corner2.x)
        min_y, max_y = min(corner1.y, corner2.y), max(corner1.y, corner2.y)

        corners = [
            Vector2D(min_x, min_y),
            Vector2D(max_x, min_y),
            Vector2D(max_x, max_y),
            Vector2D(min_x, max_y),
        ]

        return (
            all(self.point_inside(corner) for corner in corners)
            and not self.horizontal_edge_crosses(min_x, max_x, min_y)
            and not self.horizontal_edge_crosses(min_x, max_x, max_y)
            and not self.vertical_edge_crosses(min_x, min_y, max_y)
            and not self.vertical_edge_crosses(max_x, min_y, max_y)
        )


def part_2(text, example: bool = False):
    vectors = [Vector2D(*map(int, line.split(","))) for line in text.splitlines()]
    polygon = OrthogonalPolygon(vectors)

    areas = []
    for v1, v2 in combinations(vectors, 2):
        rectangle = v2 - v1
        areas.append(((abs(rectangle.x) + 1) * (abs(rectangle.y) + 1), v1, v2))

    areas.sort(reverse=True)
    for area, v1, v2 in areas:
        if polygon.rectangle_inside(v1, v2):
            return area

    raise ValueError("no value found")
