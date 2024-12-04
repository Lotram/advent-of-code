from queue import Queue

from pydantic import BaseModel, ConfigDict, Field


def get_parameter_modes(value, length):
    value //= 100
    for _ in range(length):
        yield value % 10
        value //= 10


class IntCodeComputer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    codes: list[int]
    pointer: int = 0
    name: str = "main"
    input_queue: Queue = Field(default_factory=Queue)
    output_queue: Queue = Field(default_factory=Queue)

    @classmethod
    def from_text(cls, text):
        return cls(codes=list(map(int, text.strip().split(","))))

    def get_addresses(self, modes):
        for position, mode in zip(range(len(modes)), modes, strict=True):
            address = self.pointer + position + 1
            match mode:
                case 0:
                    yield self.codes[address]
                case 1:
                    yield address
                case _:
                    raise ValueError(f"wrong mode {mode}")

    def run(self, block=False, timeout=None):
        while True:
            value = self.codes[self.pointer]
            opcode = value % 100
            match opcode:
                case 1:
                    modes = list(get_parameter_modes(value, 3))
                    addresses = list(self.get_addresses(modes))
                    self.codes[addresses[2]] = (
                        self.codes[addresses[0]] + self.codes[addresses[1]]
                    )
                    self.pointer += 4
                case 2:
                    modes = list(get_parameter_modes(value, 3))
                    addresses = list(self.get_addresses(modes))
                    self.codes[addresses[2]] = (
                        self.codes[addresses[0]] * self.codes[addresses[1]]
                    )
                    self.pointer += 4
                case 3:
                    modes = list(get_parameter_modes(value, 1))
                    assert modes == [0]
                    address = next(self.get_addresses(modes))
                    self.codes[address] = self.input_queue.get(block, timeout)
                    self.pointer += 2
                case 4:
                    modes = list(get_parameter_modes(value, 1))
                    address = next(self.get_addresses(modes))

                    self.output_queue.put(self.codes[address])
                    self.pointer += 2
                case 5:
                    modes = list(get_parameter_modes(value, 2))
                    addresses = list(self.get_addresses(modes))
                    if self.codes[addresses[0]] != 0:
                        self.pointer = self.codes[addresses[1]]
                    else:
                        self.pointer += 3
                case 6:
                    modes = list(get_parameter_modes(value, 2))
                    addresses = list(self.get_addresses(modes))
                    if self.codes[addresses[0]] == 0:
                        self.pointer = self.codes[addresses[1]]
                    else:
                        self.pointer += 3
                case 7:
                    modes = list(get_parameter_modes(value, 3))
                    addresses = list(self.get_addresses(modes))
                    self.codes[addresses[2]] = int(
                        self.codes[addresses[0]] < self.codes[addresses[1]]
                    )
                    self.pointer += 4
                case 8:
                    modes = list(get_parameter_modes(value, 3))
                    addresses = list(self.get_addresses(modes))
                    self.codes[addresses[2]] = int(
                        self.codes[addresses[0]] == self.codes[addresses[1]]
                    )
                    self.pointer += 4
                case 99:
                    break
                case _:
                    raise ValueError()
        return