from itertools import batched
from threading import Thread
from time import sleep

import numpy as np
from pycli.src.grid import Grid, Vector
from pydantic import BaseModel, ConfigDict
from rich.live import Live

from .intcode import BaseIntCodeComputer, ListIOHandler


TILES = [" ", "#", "x", "-", "O"]


def build_grid(tiles):
    grid = Grid(np.zeros((20, 44), dtype=str))

    for t in tiles:
        grid[t[1], t[0]] = TILES[t[2]]

    grid.print()
    return grid


def sign(ball_col, paddle_col):
    return int(ball_col > paddle_col) - int(paddle_col > ball_col)


class State:
    grid: Grid
    score: int

    def __init__(self):
        self.grid = Grid(np.full((20, 44), " "))
        self.score = 0

    @property
    def ball_position(self):
        return self.grid.find("O")

    @property
    def paddle_position(self):
        return self.grid.find("-")

    def joystick_position(self):
        return sign(self.ball_position.col, self.paddle_position.col)


class IOHandler(ListIOHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = State()

    def output(self, value):
        super().output(value)
        if len(self.outputs) < 3:
            return

        col = self.get()
        row = self.get()
        tile_id = self.get()

        if col == -1 and row == 0:
            self.state.score = tile_id

        else:
            self.state.grid[row, col] = TILES[tile_id]

    def get_input(self):
        return self.state.joystick_position()


class PrintIOHandler(IOHandler):
    def __init__(self, *args, live, **kwargs):
        super().__init__(*args, **kwargs)
        self.live = live

    def output(self, value):
        super().output(value)
        sleep(0.01)
        self.live.update(self.state.grid)


class Game(BaseIntCodeComputer[IOHandler]):
    pass


class GameWithPrint(BaseIntCodeComputer[PrintIOHandler]):
    pass


def part_1(text, example: bool = False):
    computer = Game.from_text(text, io_handler=IOHandler())
    computer.run()
    result = len(computer.io_handler.state.grid.find_all("x"))
    return result


def run_game(computer):
    computer.run(block=True, timeout=10, send_stop_value=True)


def part_2(text, example: bool = False):
    with Live() as live:
        # computer = GameWithPrint.from_text(text, io_handler=PrintIOHandler(live=live))
        computer = Game.from_text(text, io_handler=IOHandler())
        computer.memory[0] = 2
        computer.run()

    return computer.io_handler.state.score
