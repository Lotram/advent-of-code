from threading import Thread

from pycli.src.grid import Grid

from .intcode import FINISHED, IntCodeComputer


directions = [1j, -1j]


def run_robot(computer):
    computer.run(block=True, timeout=3, send_stop_value=True)


def paint(text, start_color):
    computer = IntCodeComputer.from_text(text)
    direction = 1j
    position = 0
    white_panels = {0} if start_color else set()
    visited_panels = set()
    thread = Thread(target=run_robot, args=[computer])
    thread.start()

    while True:
        is_white = int(position in white_panels)
        computer.put(is_white)
        paint_color = computer.get(block=True, timeout=2)

        # stop value
        if paint_color is FINISHED:
            break

        visited_panels.add(position)
        if paint_color:
            white_panels.add(position)
        elif is_white:
            white_panels.remove(position)

        turn = computer.get(block=True, timeout=2)
        direction *= directions[turn]
        position += direction

    return white_panels, visited_panels


def part_1(text, example: bool = False):
    _, visited_panels = paint(text, 0)
    result = len(visited_panels)
    return result


def part_2(text, example: bool = False):
    white_panels, _ = paint(text, 1)

    Grid.from_complex_values(white_panels).print()

    result = "RFEPCFEB"
    return result
