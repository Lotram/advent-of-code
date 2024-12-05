from collections import defaultdict
from queue import Queue

from pydantic import BaseModel, ConfigDict, Field


class Finished(Exception):
    pass


param_count_by_op_codes = {1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1, 99: 0}


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


class IntCodeComputer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    memory: Memory
    pointer: int = 0
    relative_base: int = 0
    name: str = "main"
    input_queue: Queue = Field(default_factory=Queue)
    output_queue: Queue = Field(default_factory=Queue)

    def reset(self):
        self.pointer = 0
        self.relative_base = 0
        self.memory.reset()

    def get(self, block=False, timeout=None):
        return self.output_queue.get(block=block, timeout=timeout)

    def get_all(self):
        outputs = []
        while not self.output_queue.empty():
            outputs.append(self.get())
        return outputs

    def put(self, item):
        return self.input_queue.put(item)

    @classmethod
    def from_text(cls, text):
        codes = list(map(int, text.strip().split(",")))
        return cls(memory=Memory(codes))

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

    def run(self, block=False, timeout=None):
        while True:
            try:
                self._run(block=block, timeout=timeout)
            except Finished:
                return

    def _run(self, block=False, timeout=None):
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
                self.memory[addresses[0]] = self.input_queue.get(block, timeout)

            case 4:
                # output
                self.output_queue.put(self.memory[addresses[0]])

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
                raise Finished()
            case _:
                raise ValueError()

        if not pointer_has_changed:
            self.pointer += len(modes) + 1
