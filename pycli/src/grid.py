from collections.abc import Collection
from itertools import starmap
from typing import NamedTuple, Self

import numpy as np


class VectorMixin:
    @property
    def fields(self):
        return self._fields

    def __add__(self, vec: Self) -> Self:
        kwargs = {
            field: getattr(self, field) + getattr(vec, field) for field in self.fields
        }
        return self.__class__(**kwargs)

    def __sub__(self, other: Self) -> Self:
        return self.__add__(-other)

    def __neg__(self):
        return self * -1

    def __mul__(self, value: int) -> Self:
        kwargs = {field: getattr(self, field) * value for field in self.fields}
        return self.__class__(**kwargs)

    def __rmul__(self, value: int) -> Self:
        return self.__mul__(value)

    def norm(self, p=1) -> float:
        return pow(sum(pow(abs(x), p) for x in self), 1 / p)

    def __iter__(self):
        for field in self.fields:
            yield getattr(self, field)


class _Vector2D(NamedTuple):
    x: int
    y: int


class Vector2D(VectorMixin, _Vector2D):
    def rotate(self, k):
        """
        rotate by 90 degres, clockwise
        """
        match k % 4:
            case 0:
                values = (self[0], self[1])
            case 1:
                values = (self[1], -self[0])
            case 2:
                values = (-self[0], -self[1])
            case 3:
                values = (-self[1], self[0])
        return self.__class__(*values)


class Particle2D(NamedTuple):
    position: Vector2D
    speed: Vector2D
    acceleration: Vector2D

    def get_position(self, t) -> int:
        return self.position + t * self.speed + t * (t + 1) // 2 * self.acceleration

    def get_speed(self, t) -> int:
        return self.speed + t * self.acceleration


class _Vector3D(NamedTuple):
    x: int
    y: int
    z: int


class Vector3D(VectorMixin, _Vector3D):
    pass


# FIXME: legacy, should be removed
class _Vector(NamedTuple):
    row: int
    col: int


class Vector(VectorMixin, _Vector):
    def rotate(self, k):
        """
        rotate by 90 degres, clockwise
        """
        match k % 4:
            case 0:
                values = (self[0], self[1])
            case 1:
                values = (self[1], -self[0])
            case 2:
                values = (-self[0], -self[1])
            case 3:
                values = (-self[1], self[0])
        return self.__class__(*values)


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

    @classmethod
    def from_text(cls, text, diag=False):
        array = np.array(list(map(list, text.strip().split("\n"))))
        return cls(array, diag=diag)

    @classmethod
    def from_complex_values(cls, values: Collection[complex]):
        min_col = int(min(c.real for c in values))
        max_col = int(max(c.real for c in values))
        max_row = int(max(c.imag for c in values))
        min_row = int(min(c.imag for c in values))
        row_size = max_row - min_row + 1
        col_size = max_col - min_col + 1
        array = np.zeros((row_size, col_size), dtype=bool)
        for val in values:
            array[max_row - int(val.imag)][int(val.real - min_col)] = True

        return cls(array)

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
        return 0 <= vector[0] < self.row_size and 0 <= vector.col < self.col_size

    def contains(self, vector: Vector):
        return vector in self

    def neighbours(self, vector: Vector):
        directions = DIRECTIONS + DIAG_DIRECTIONS if self.diag else DIRECTIONS
        for direction in directions:
            neighbour = vector + direction
            if self.contains(neighbour):
                yield (neighbour, self[neighbour])

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
        return starmap(Vector, zip(*np.where(self.arr == value), strict=False))

    def find(self, value):
        return next(self.find_iter(value))

    def find_all(self, value):
        return list(self.find_iter(value))

    def replace(self, old, new):
        self.arr[self.arr == old] = new

    def rot90(self, k):
        self.arr = np.rot90(self.arr, k)

    def print(self, file=None):
        if self.arr.dtype == "bool":
            rows = iter(np.where(self.arr, "#", "."))
        else:
            rows = self.rows
        for row in rows:
            print("".join(map(str, row)), file=file)

    def transpose(self):
        return Grid(self.arr.transpose(), self.diag)


def complex_from_positions(row_idx, col_idx, row_count):
    return col_idx + (row_count - row_idx - 1) * 1j
