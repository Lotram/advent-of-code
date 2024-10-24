from dataclasses import astuple, dataclass
from itertools import count

import numpy as np
from pycli.src.grid import EAST, NORTH, SOUTH, WEST, Grid, Vector


@dataclass(slots=True)
class Cart:
    position: Vector
    direction: Vector
    idx: int
    next_rotation: int = -1

    def move(self, grid):
        char = grid[self.position]
        match char:
            case "-" | "|":
                pass
            case "/":
                self.direction = Vector(-self.direction.col, -self.direction.row)

            case "\\":
                self.direction = Vector(self.direction.col, self.direction.row)

            case "+":
                self.direction = self.direction.rotate(self.next_rotation)
                self.next_rotation = (self.next_rotation + 2) % 3 - 1

            case _:
                raise RuntimeError(f"Invalid char: {char} at position {self.position}")

        self.position += self.direction

    def find_loop(self, grid):
        tick = 0
        states = {astuple(self): tick}
        while True:
            tick += 1
            self.move(grid)
            state = astuple(self)
            if state in states:
                return (
                    {(_state[0], time) for _state, time in states.items()},
                    state[0],
                    states[state],
                    tick,
                )
            states[state] = tick


def parse_grid(text) -> Grid:
    return Grid(np.array(list(map(list, text.rstrip("\n").split("\n")))))


def get_carts(grid):
    idx = count()
    carts = [
        Cart(position=position, direction=direction, idx=next(idx))
        for char, direction in (
            (">", EAST),
            ("<", WEST),
            ("^", NORTH),
            ("v", SOUTH),
        )
        for position in grid.find_all(char)
    ]
    grid.replace(">", "-")
    grid.replace("<", "-")
    grid.replace("^", "|")
    grid.replace("v", "|")
    return {cart.position: cart for cart in carts}


def part_1(text, example: bool = False):
    grid = parse_grid(text)
    carts = get_carts(grid)
    while True:
        for cart_position in sorted(carts):
            cart = carts.pop(cart_position)

            cart.move(grid)
            if cart.position in carts:
                return f"{cart.position.col},{cart.position.row}"
            carts[cart.position] = cart


def part_2(text, example: bool = False):
    grid = parse_grid(text)
    carts = get_carts(grid)

    while True:
        for cart_position in sorted(carts):
            cart = carts.pop(cart_position, None)
            if cart is None:
                # cart just crashed
                continue

            cart.move(grid)
            if cart.position in carts:
                del carts[cart.position]
            else:
                carts[cart.position] = cart
        if len(carts) == 1:
            cart = list(carts.values())[0]
            return f"{cart.position.col},{cart.position.row}"
