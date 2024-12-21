import threading
from functools import partial

from pycli.src.dijkstra import dijkstra

from .intcode import Finished, QueueIntCodeComputer


directions = {1j: 1, -1j: 2, 1: 3, -1: 4}

START = 0


class Droid(QueueIntCodeComputer):
    visited: set[complex] = set()
    path: list[complex] = []
    part: int = 1
    oxygen_position: complex | None = None

    def move(self, direction):
        self.put(directions[direction])
        return self.get()

    def stop(self):
        self.io_handler.stop_event.set()
        self.put(directions[1])

    def explore(self, position):
        try:
            self._explore(position)
            self.stop()
        except Finished:
            return

    def _explore(self, position):
        self.visited.add(position)
        self.path.append(position)

        for direction in directions:
            neighbour = position + direction
            if neighbour not in self.visited:
                response = self.move(direction)
                match response:
                    case 0:
                        pass

                    case 1:
                        val = self._explore(neighbour)
                        if val is not None and self.part == 1:
                            return val
                        self.move(-direction)
                        self.path.pop()

                    case 2:
                        self.oxygen_position = neighbour

                        if self.part == 1:
                            self.stop()
                            raise Finished()
                        else:
                            val = self._explore(neighbour)
                            self.move(-direction)
                            self.path.pop()


def part_1(text, example: bool = False):
    droid = Droid.from_text(text)
    thread = threading.Thread(target=droid.run)
    thread.start()

    droid.explore(START)
    return len(droid.path)


def get_neighbours(locations, position):
    for direction in directions:
        if (neighbour := position + direction) in locations:
            yield (neighbour, 1)


def part_2(text, example: bool = False):
    droid = Droid.from_text(text)
    droid.part = 2

    thread = threading.Thread(target=droid.run)
    thread.start()
    result = droid.explore(START)
    min_dist = dijkstra(
        droid.oxygen_position,
        stop_condition=lambda current: False,
        get_neighbours=partial(get_neighbours, droid.visited),
        return_all=True,
    )
    result = max(min_dist.values())
    return result
