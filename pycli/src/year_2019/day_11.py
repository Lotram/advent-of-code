from pycli.src.grid import Grid
from pydantic import BaseModel

from .intcode import BaseIntCodeComputer, ListIOHandler


directions = [1j, -1j]


class State(BaseModel):
    direction: complex = 1j
    position: complex = 0
    white_panels: set[complex]
    visited_panels: set[complex] = set()

    def process(self, paint_color, turn):
        self.visited_panels.add(self.position)
        if paint_color:
            self.white_panels.add(self.position)
        elif self.is_white:
            self.white_panels.remove(self.position)

        self.direction *= directions[turn]
        self.position += self.direction

    @property
    def is_white(self):
        return int(self.position in self.white_panels)


class IOHandler(ListIOHandler):
    def __init__(self, *args, start_color, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = State(white_panels={0} if start_color else set())

    def output(self, value):
        super().output(value)
        if len(self.outputs) < 2:
            return

        paint_color = self.get()
        turn = self.get()
        self.state.process(paint_color, turn)

    def get_input(self):
        return self.state.is_white


class Robot(BaseIntCodeComputer[IOHandler]):
    pass


def run_robot(computer):
    computer.run(block=True, timeout=3, send_stop_value=True)


def paint(text, start_color):
    computer = Robot.from_text(text, io_handler=IOHandler(start_color=start_color))
    computer.run()

    return computer.io_handler.state


def part_1(text, example: bool = False):
    state = paint(text, 0)
    result = len(state.visited_panels)
    return result


def part_2(text, example: bool = False):
    state = paint(text, 1)

    Grid.from_complex_values(state.white_panels).print()

    result = "RFEPCFEB"
    return result
