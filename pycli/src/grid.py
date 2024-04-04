from dataclasses import dataclass
from itertools import starmap

import numpy as np


class AbstractVector:

    @property
    def fields(self):
        return tuple(self.__dataclass_fields__)

    def __add__(self, vec: "AbstractVector") -> "AbstractVector":
        kwargs = {
            field: getattr(self, field) + getattr(vec, field) for field in self.fields
        }
        return self.__class__(**kwargs)

    def __sub__(self, other: "AbstractVector") -> "AbstractVector":
        return self.__add__(-other)

    def __neg__(self):
        return self * -1

    def __mul__(self, value: int) -> "AbstractVector":
        kwargs = {field: getattr(self, field) * value for field in self.fields}
        return self.__class__(**kwargs)

    def __rmul__(self, value: int) -> "AbstractVector":
        return self.__mul__(value)

    def norm(self, p=1):
        return pow(sum(pow(abs(x), p) for x in self), 1 / p)

    def __iter__(self):
        for field in self.fields:
            yield getattr(self, field)


@dataclass(slots=True)
class Vector2D(AbstractVector):
    x: int
    y: int


@dataclass(slots=True)
class Vector3D(Vector2D):
    z: int


# FIXME: legacy, should be removed
@dataclass(slots=True)
class Vector(AbstractVector):
    row: int
    col: int


DIRECTIONS = [
    NORTH := Vector(-1, 0),
    EAST := Vector(0, 1),
    SOUTH := Vector(1, 0),
    WEST := Vector(0, -1),
]
DIAG_DIRECTIONS = [Vector(-1, -1), Vector(1, -1), Vector(-1, 1), Vector(1, 1)]


# TODO: make this work with 3D ?
# TODO: make this work with (x, y) instead of (row, col) ?
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

    def __contains__(self, vector: Vector) -> bool:
        return 0 <= vector.row < self.row_size and 0 <= vector.col < self.col_size

    def contains(self, vector: Vector):
        return vector in self

    def neighbours(self, vector: Vector):
        directions = DIRECTIONS + DIAG_DIRECTIONS if self.diag else DIRECTIONS
        for direction in directions:
            neighbour = vector + direction
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
            (Vector(row_idx, col_idx), val)
            for row_idx, row in enumerate(self.rows)
            for col_idx, val in enumerate(row)
        )

    def find_iter(self, value):
        return starmap(Vector, zip(*np.where(self.arr == value)))

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
        return Grid(self.arr.transpose(), self.diag)
