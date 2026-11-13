import threading
from queue import Empty, Queue
from typing import Any

from pycli.src.year_2019.intcode import BaseIntCodeComputer, Memory, QueueIOHandler


class Handler(QueueIOHandler):
    def __init__(
        self,
        input_queue: Queue | None = None,
        output_queue: Queue | None = None,
        get_kwargs: dict[str, Any] | None = None,
        stop_event=None,
        *,
        idx: int,
    ):
        super().__init__(input_queue, output_queue, get_kwargs, stop_event)
        self.idx = idx
        self.packet = []
        self.idle = False

    def get_input(self):
        try:
            value = self.input_queue.get(block=True, timeout=0.1)
            self.idle = False

        except Empty:
            value = -1
            self.idle = True

        return value

    def output(self, item):
        self.packet.append(item)
        if len(self.packet) == 3:
            super().output(tuple(self.packet))
            self.packet.clear()


class NIC(BaseIntCodeComputer[Handler]):
    def should_stop(self):
        return self.io_handler.stop_event.is_set()

    @classmethod
    def from_text(cls, text, io_handler: Handler):
        codes = list(map(int, text.strip().split(",")))
        return cls(memory=Memory(codes), io_handler=io_handler)

    @property
    def idle(self):
        return self.io_handler.idle


def part_1(text, example: bool = False):
    main_queue = Queue()
    computers = []
    for idx in range(50):
        handler = Handler(output_queue=main_queue, idx=idx)
        handler.input_queue.put(idx)
        computer = NIC.from_text(text, handler)
        computers.append(computer)
        thread = threading.Thread(target=computer.run)
        thread.start()

    while True:
        address, X, Y = main_queue.get(timeout=10)
        if address == 255:
            for computer in computers:
                computer.io_handler.stop_event.set()
            return Y

        computers[address].put(X)
        computers[address].put(Y)


def part_2(text, example: bool = False):
    main_queue = Queue()
    computers = []
    nat_x = nat_y = None
    values = []
    for idx in range(50):
        handler = Handler(output_queue=main_queue, idx=idx)
        handler.input_queue.put(idx)
        computer = NIC.from_text(text, handler)
        computers.append(computer)
        thread = threading.Thread(target=computer.run)
        thread.start()

    while True:
        if all(computer.idle for computer in computers) and nat_y:
            if values and values[-1] == nat_y:
                for computer in computers:
                    computer.io_handler.stop_event.set()
                return nat_y
            address, X, Y = 0, nat_x, nat_y
            values.append(nat_y)
            nat_y = None

        else:
            try:
                address, X, Y = main_queue.get(timeout=0.1)
            except:
                continue
            if address == 255:
                nat_x = X
                nat_y = Y
                continue

        computers[address].put(X)
        computers[address].put(Y)
