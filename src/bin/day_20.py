import time
from collections import defaultdict, deque
from functools import cache, cached_property
from itertools import filterfalse, tee
from math import lcm
from operator import attrgetter, methodcaller
from typing import Annotated, Literal

from pydantic import BaseModel, Field


def partition(pred, iterable):
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


class Module(BaseModel):
    name: str
    type: str
    destinations: list[str] = []

    def transmit(self, pulse: "Pulse") -> "list[Pulse]":
        value = self.get_value(pulse)
        if value is None:
            return []

        return [
            Pulse(
                origin=self.name, value=value, destination=dest, counter=pulse.counter
            )
            for dest in self.destinations
        ]


class Pulse(BaseModel):
    value: bool
    origin: str
    destination: str
    counter: int | None = None

    def __str__(self):
        value = "high" if self.value else "low"
        return f"{self.origin} -{value}-> {self.destination}"


class Broadcaster(Module):
    name: str = "broadcaster"
    type: Literal["broadcaster"] = "broadcaster"

    def get_value(self, pulse):
        return pulse.value


class FlipFlop(Module):
    state: bool = False
    type: Literal["flipflop"] = "flipflop"

    def get_value(self, pulse):
        if pulse.value:
            return

        self.state = not self.state
        return self.state


class Conjunction(Module):
    state: dict[str, bool] = {}
    type: Literal["conjunction"] = "conjunction"
    cycle: int | None = None

    def get_value(self, pulse):
        self.state[pulse.origin] = pulse.value
        value = not all(self.state.values())
        if value and not self.cycle:
            self.cycle = pulse.counter
            print(f"{self.name}: {self.cycle}")
        return value


class Output(Module):
    type: Literal["output"] = "output"

    def get_value(self, pulse):
        return None


ModuleT = Annotated[
    Broadcaster | FlipFlop | Conjunction | Output, Field(discriminator="type")
]


class State(BaseModel):
    modules: list[ModuleT]

    @cached_property
    def modules_by_name(self):
        return {module.name: module for module in self.modules}

    def get(self, name):
        return self.modules_by_name.get(name)

    def __eq__(self, other):
        return self.modules == other.modules


def parse(lines):
    broadcaster = None
    modules = []
    predecessor_by_name = defaultdict(list)
    for line in lines:
        mod, destinations = map(methodcaller("strip"), line.split(" -> "))
        destinations = destinations.split(", ")
        if mod == "broadcaster":
            broadcaster = Broadcaster(name="broadcaster")
            module = broadcaster
        elif mod.startswith("%"):
            module = FlipFlop(name=mod[1:])

        elif mod.startswith("&"):
            module = Conjunction(name=mod[1:])
        else:
            raise ValueError(mod)

        module.destinations = destinations
        modules.append(module)

        for destination in destinations:
            predecessor_by_name[destination].append(module.name)

    state = State(modules=modules)

    for module in state.modules:
        if isinstance(module, Conjunction):
            for predecessor in predecessor_by_name[module.name]:
                module.state[predecessor] = False

    outputs = set(predecessor_by_name) - {module.name for module in state.modules}
    for output in outputs:
        state.modules.append(Output(name=output))

    return state


def push_button(state, counter):
    signals = deque(
        [
            Pulse(
                origin="button", value=False, destination="broadcaster", counter=counter
            )
        ]
    )
    values = []
    while signals:
        signal = signals.popleft()

        values.append(signal.value)
        destination = state.get(signal.destination)
        if destination is not None:
            signals.extend(destination.transmit(signal))

    high, low = partition(bool, values)
    return len(list(high)), len(list(low))


def part_1(text):
    lines = text.strip().split("\n")
    state = parse(lines)
    high, low = (0, 0)
    for _ in range(1000):
        _high, _low = push_button(state)
        high += _high
        low += _low

    result = high * low

    print(result)


def part_2(text):
    lines = text.strip().split("\n")
    state = parse(lines)
    counter = 0

    rx_parent_name = next(
        mod.name for mod in state.modules if mod.destinations == ["rx"]
    )

    rx_grand_parent_names = [
        mod.name for mod in state.modules if mod.destinations == [rx_parent_name]
    ]
    while True:
        counter += 1
        push_button(state, counter)

        if all(state.get(name).cycle for name in rx_grand_parent_names):
            result = lcm(*[state.get(name).cycle for name in rx_grand_parent_names])
            break

        if counter > 20_000:
            break
    print(result)


def draw_graph(state):
    for module in state.modules:
        for dest in module.destinations:
            print(f"{module.name} --> {dest}")
        print(f"class {module.name} {module.type}")
