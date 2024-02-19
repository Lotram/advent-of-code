from typing import NamedTuple

import numpy as np


class Point(NamedTuple):
    row: int
    col: int

    def __add__(self, vec: "Vector") -> "Point":
        return Point(self.row + vec.row, self.col + vec.col)


class Vector(Point):
    pass

    def __mul__(self, value: int) -> "Vector":
        return Vector(self.row * value, self.col * value)

    def __rmul__(self, value: int) -> "Vector":
        return self.__mul__(value)

    def __add__(self, point: "Point") -> "Point":
        return Point(self.row + point.row, self.col + point.col)


DIRECTIONS = [
    NORTH := Vector(-1, 0),
    EAST := Vector(0, 1),
    SOUTH := Vector(1, 0),
    WEST := Vector(0, -1),
]
DIAG_DIRECTIONS = [Vector(-1, -1), Vector(1, -1), Vector(-1, 1), Vector(1, 1)]


class Grid:
    def __init__(self, arr, diag=False):
        self.arr = np.array(arr)
        self.diag = diag

    def __getitem__(self, item):
        return self.arr.__getitem__(item)

    def __setitem__(self, item, value):
        return self.arr.__setitem__(item, value)

    @property
    def row_size(self):
        return len(self.arr)

    @property
    def col_size(self):
        return len(self.arr[0])

    def contains(self, point: Point):
        return 0 <= point[0] < self.row_size and 0 <= point[1] < self.col_size

    def neighbours(self, point: Point):
        directions = DIRECTIONS + DIAG_DIRECTIONS if self.diag else DIRECTIONS
        for direction in directions:
            neighbour = point + direction
            if self.contains(neighbour):
                yield (neighbour, self.arr[neighbour])

    @property
    def rows(self):
        yield from self.arr

    def get_row(self, idx):
        return self.arr[idx]

    @property
    def columns(self):
        yield from self.arr.transpose()

    def get_col(self, idx):
        return self.arr[:, idx]

    def flat_iter(self):
        yield from (
            (Point(row_idx, col_idx), val)
            for row_idx, row in enumerate(self.rows)
            for col_idx, val in enumerate(row)
        )

    def find_iter(self, value):
        # return (point for point, _value in self.flat_iter() if _value == value)
        return zip(*np.where(self.arr == "*"))

    def find(self, value):
        return next(self.find_iter(value))

    def find_all(self, value):
        return list(self.find_iter(value))

    def replace(self, old, new):
        self.arr[self.arr == old] = new

    def rotate(self, idx, shift, axis):
        """
        axis 0 to rotate a row, 1 to rotate a column
        """
        _slice = idx if axis == 0 else (slice(None), idx)
        self.arr[_slice] = np.roll(self.arr[_slice], shift=shift)

    def print(self):
        if self.arr.dtype == "bool":
            rows = iter(np.where(self.arr, "#", "."))
        else:
            rows = self.rows
        for row in rows:
            print("".join(map(str, row)))

    def transpose(self):
        return Grid(self.arr.transpose, self.diag)
