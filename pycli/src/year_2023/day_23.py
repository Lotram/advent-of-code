from collections import defaultdict, deque
from typing import NamedTuple


inf = float("inf")


class Point(NamedTuple):
    row: int
    col: int


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = {UP, LEFT, RIGHT, DOWN}
valid_predecessor = {"<": {RIGHT}, ">": {LEFT}, "v": {UP}, "^": {DOWN}, ".": DIRECTIONS}


class Path(NamedTuple):
    head: Point
    tail: set[Point]
    subpath_start: Point


# TODO replace with grid file
class Grid:
    def __init__(self, lines, part):
        self.row_size = len(lines)
        self.col_size = len(lines[0])
        self.parse(lines)
        self.part = part

    def parse(self, lines):
        self.start = Point(0, lines[0].find("."))
        self.end = Point(self.row_size - 1, lines[-1].find("."))
        self.grid = {
            Point(row, col): char
            for row, line in enumerate(lines)
            for col, char in enumerate(line)
            if char != "#"
        }

    def get_predecessors(self, path: Path):
        row, col = path.head
        predecessors = []
        for direction in DIRECTIONS:
            neighbour = row + direction[0], col + direction[1]
            char = self.grid.get(neighbour)
            if char is None or neighbour in path.tail:
                continue
            if self.part == 2 or direction in valid_predecessor[char]:
                predecessors.append(Path(neighbour, path.tail | {path.head}, neighbour))
        return predecessors

    def get_longest_path(self):
        queue = deque([Path(self.end, set(), self.end)])
        result = 0
        while queue:
            path = queue.popleft()
            while True:
                try:
                    path, *other_predecessors = self.get_predecessors(path)
                except ValueError:  # end of path
                    if path.head == self.start:
                        result = max(result, len(path.tail))
                    break
                else:
                    queue.extend(other_predecessors)
        return result


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    grid = Grid(lines, part=1)
    return grid.get_longest_path()


class Path2(NamedTuple):
    head: Point
    body: set[Point]
    length: int


class Section(NamedTuple):
    head: Point
    previous: Point
    tail: Point
    length: int


class Grid2:
    def __init__(self, lines):
        self.row_size = len(lines)
        self.col_size = len(lines[0])
        self.parse(lines)

    def parse(self, lines):
        self.start = Point(0, lines[0].find("."))
        self.end = Point(self.row_size - 1, lines[-1].find("."))
        self.grid = {
            Point(row, col): char
            for row, line in enumerate(lines)
            for col, char in enumerate(line)
            if char != "#"
        }

    def get_neighbours(self, node, previous):
        row, col = node
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = row + direction[0], col + direction[1]
            char = self.grid.get(neighbour)
            if char is not None and neighbour != previous:
                neighbours.append(neighbour)
        return neighbours

    def get_next_sections(self, intersection, previous):
        sections = []
        for neighbour in self.get_neighbours(intersection, previous):
            if neighbour == previous:
                continue
            count = 1
            node = neighbour
            previous = intersection
            while True:
                neighbours = self.get_neighbours(node, previous)
                match len(neighbours):
                    case 0:
                        if node == self.start:
                            sections.append(
                                Section(node, previous, intersection, count)
                            )
                        else:
                            self.grid.pop(node, None)
                        break
                    case 1:
                        previous = node
                        node = neighbours[0]
                        count += 1
                    case _:
                        sections.append(Section(node, previous, intersection, count))
                        break
        return sections

    def get_graph(self):
        queue = deque(self.get_next_sections(self.end, None))
        sections = set()

        while queue:
            section = queue.popleft()
            if section in sections:
                continue
            sections.add(section)
            queue.extend(self.get_next_sections(section.head, section.previous))

        graph = defaultdict(set)
        for section in sections:
            graph[section.head].add((section.tail, section.length))
            graph[section.tail].add((section.head, section.length))

        return graph

    def get_predecessors(self, path: Path2):
        neighbours = self.graph[path.head]
        predecessors = []
        for neighbour, length in neighbours:
            if neighbour in path.body:
                continue
            predecessors.append(
                Path2(neighbour, path.body | {path.head}, path.length + length)
            )

        return predecessors

    def get_longest_path(self):
        self.graph = self.get_graph()
        queue = deque([Path2(self.end, set(), 0)])
        result = 0
        while queue:
            paths = self.get_predecessors(queue.popleft())
            for path in paths:
                if path.head == self.start:
                    result = max(result, path.length)
                else:
                    queue.append(path)

        return result


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    grid = Grid2(lines)
    return grid.get_longest_path()
