import queue
import threading
from collections import defaultdict
from dataclasses import dataclass


def part_1(text):
    registers = defaultdict(int)

    def value(x):
        return int(x) if x.lstrip("-").isdigit() else registers[x]

    instructions = list(text.strip().split("\n"))
    cursor = 0
    frequency = 0
    while 0 <= cursor < len(instructions):
        instruction = instructions[cursor]
        match instruction.split():
            case ["snd", x]:
                frequency = value(x)
            case ["set", x, y]:
                registers[x] = value(y)
            case ["add", x, y]:
                registers[x] += value(y)
            case ["mul", x, y]:
                registers[x] *= value(y)
            case ["mod", x, y]:
                registers[x] %= value(y)
            case ["rcv", x]:
                if value(x) != 0:
                    return frequency

            case ["jgz", x, y]:
                if value(x) > 0:
                    cursor += int(y) - 1

            case _:
                raise ValueError(f"unknown command: {instruction}")

        cursor += 1


@dataclass
class Process:
    pid: int
    instructions: list[str]
    registers: defaultdict[str, int]

    q: queue.Queue

    blocked: bool = False
    cursor: int = 0
    other: "Process | None" = None
    send_counter: int = 0

    def value(self, x: str) -> int:
        return int(x) if x.lstrip("-").isdigit() else self.registers[x]

    def run(self):
        assert self.other is not None
        while 0 <= self.cursor < len(self.instructions):
            instruction = self.instructions[self.cursor]
            match instruction.split():
                case ["snd", x]:
                    self.other.q.put(self.value(x))
                    self.send_counter += 1
                case ["set", x, y]:
                    self.registers[x] = self.value(y)
                case ["add", x, y]:
                    self.registers[x] += self.value(y)
                case ["mul", x, y]:
                    self.registers[x] *= self.value(y)
                case ["mod", x, y]:
                    self.registers[x] %= self.value(y)
                case ["rcv", x]:
                    try:
                        # 0.1 seconds is enough to detect a deadlock
                        item = self.q.get(timeout=0.1)
                        self.registers[x] = item
                    except queue.Empty:
                        return

                case ["jgz", x, y]:
                    if self.value(x) > 0:
                        self.cursor += self.value(y) - 1

                case _:
                    raise ValueError(f"unknown command: {instruction}")

            self.cursor += 1


def part_2(text):
    instructions = list(text.strip().split("\n"))
    p0 = Process(
        pid=0,
        instructions=instructions,
        registers=defaultdict(int),
        q=queue.Queue(),
    )
    p1 = Process(
        pid=1,
        instructions=instructions,
        other=p0,
        registers=defaultdict(int, {"p": 1}),
        q=queue.Queue(),
    )
    p0.other = p1
    t0 = threading.Thread(target=p0.run)
    t1 = threading.Thread(target=p1.run)
    t0.start()
    t1.start()
    t0.join()
    t1.join()

    result = p1.send_counter
    return result
