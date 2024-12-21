import threading
from collections import defaultdict, deque
from queue import Queue
from typing import Any

from pydantic import BaseModel, ConfigDict


class Finished(Exception):
    pass


param_count_by_op_codes = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}

FINISHED = object()


class Memory:
    def __init__(self, codes: list[int]):
        self.initial_state = codes
        self.reset()

    def __getitem__(self, key: int) -> int:
        if key < 0:
            raise ValueError("memory index must be positive")

        return self._memory.__getitem__(key)

    def __setitem__(self, key: int, value: int):
        if key < 0:
            raise ValueError("memory index must be positive")

        return self._memory.__setitem__(key, value)

    def reset(self):
        self._memory = defaultdict(int, dict(enumerate(self.initial_state)))


class BaseIOHandler:
    def put(self, value: int):
        raise NotImplementedError()

    def get_input(self) -> int:
        raise NotImplementedError()

    def output(self, value: int):
        raise NotImplementedError()

    def get(self) -> int:
        raise NotImplementedError()

    def get_all(self) -> list[int]:
        raise NotImplementedError()


class ListIOHandler(BaseIOHandler):
    def __init__(self, inputs: list[int] | None = None):
        self.inputs = deque(inputs or [])
        self.outputs = deque()

    def put(self, value):
        self.inputs.append(value)

    def get_input(self) -> int:
        return self.inputs.popleft()

    def output(self, value: int):
        self.outputs.append(value)

    def get(self) -> int:
        return self.outputs.popleft()

    def get_all(self) -> list[int]:
        outputs = list(self.outputs)
        self.outputs = deque()
        return outputs


class QueueIOHandler(BaseIOHandler):
    def __init__(
        self,
        input_queue: Queue | None = None,
        output_queue: Queue | None = None,
        get_kwargs: dict[str, Any] | None = None,
        stop_event=None,
    ):
        self.input_queue = input_queue or Queue()
        self.output_queue = output_queue or Queue()
        self.get_kwargs = get_kwargs or {}
        self.stop_event = stop_event or threading.Event()

    def put(self, item):
        return self.input_queue.put(item)

    def get_input(self):
        return self.input_queue.get(**self.get_kwargs)

    def output(self, item):
        self.output_queue.put(item)

    def get(self):
        return self.output_queue.get(**self.get_kwargs)

    def get_all(self):
        outputs = []
        while not self.output_queue.empty():
            outputs.append(self.get())
        return outputs


class BaseIntCodeComputer[IOHandler: BaseIOHandler](BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    memory: Memory
    io_handler: IOHandler
    pointer: int = 0
    relative_base: int = 0
    name: str = "main"

    def reset(self):
        self.pointer = 0
        self.relative_base = 0
        self.memory.reset()

    def halt(self):
        pass

    def put(self, value):
        self.io_handler.put(value)

    def get_input(self):
        return self.io_handler.get_input()

    def output(self, item):
        self.io_handler.output(item)

    def get(self):
        return self.io_handler.get()

    def get_all(self):
        return self.io_handler.get_all()

    def should_stop(self):
        return False

    @classmethod
    def from_text(cls, text, io_handler: IOHandler):
        codes = list(map(int, text.strip().split(",")))
        return cls(memory=Memory(codes), io_handler=io_handler)

    def get_values(self):
        value = self.memory[self.pointer]
        opcode = value % 100
        length = param_count_by_op_codes[opcode]
        value //= 100
        modes = []
        for _ in range(length):
            modes.append(value % 10)
            value //= 10

        return opcode, modes

    def get_addresses(self, modes):
        addresses = []
        for position, mode in zip(range(len(modes)), modes, strict=True):
            _address = self.pointer + position + 1
            match mode:
                case 0:
                    address = self.memory[_address]
                case 1:
                    address = _address
                case 2:
                    address = self.memory[_address] + self.relative_base
                case _:
                    raise ValueError(f"wrong mode {mode}")

            addresses.append(address)
        return addresses

    def run(self):
        while not self.should_stop():
            try:
                self._run()
            except Finished:
                return

    def _run(self):
        opcode, modes = self.get_values()
        addresses = self.get_addresses(modes)
        pointer_has_changed = False
        match opcode:
            case 1:
                # Addition
                self.memory[addresses[2]] = (
                    self.memory[addresses[0]] + self.memory[addresses[1]]
                )

            case 2:
                # multiplication
                self.memory[addresses[2]] = (
                    self.memory[addresses[0]] * self.memory[addresses[1]]
                )

            case 3:
                # get input
                assert not (set(modes) & {1})
                self.memory[addresses[0]] = self.get_input()

            case 4:
                # output
                self.output(self.memory[addresses[0]])

            case 5:
                # jump if true
                if self.memory[addresses[0]] != 0:
                    self.pointer = self.memory[addresses[1]]
                    pointer_has_changed = True

            case 6:
                # jump if false
                if self.memory[addresses[0]] == 0:
                    self.pointer = self.memory[addresses[1]]
                    pointer_has_changed = True

            case 7:
                # less than
                self.memory[addresses[2]] = int(
                    self.memory[addresses[0]] < self.memory[addresses[1]]
                )

            case 8:
                # equals
                self.memory[addresses[2]] = int(
                    self.memory[addresses[0]] == self.memory[addresses[1]]
                )

            case 9:
                # set relative base
                self.relative_base += self.memory[addresses[0]]

            case 99:
                self.halt()
                raise Finished()
            case _:
                raise ValueError()

        if not pointer_has_changed:
            self.pointer += len(modes) + 1


class ListIntCodeComputer(BaseIntCodeComputer[ListIOHandler]):
    @classmethod
    def from_text(cls, text, io_handler: ListIOHandler | None = None):
        codes = list(map(int, text.strip().split(",")))
        if io_handler is None:
            io_handler = ListIOHandler()
        return cls(memory=Memory(codes), io_handler=io_handler)


class QueueIntCodeComputer(BaseIntCodeComputer[QueueIOHandler]):
    def should_stop(self):
        return self.io_handler.stop_event.is_set()

    @classmethod
    def from_text(cls, text, io_handler: QueueIOHandler | None = None):
        codes = list(map(int, text.strip().split(",")))
        if io_handler is None:
            io_handler = QueueIOHandler()
        return cls(memory=Memory(codes), io_handler=io_handler)
