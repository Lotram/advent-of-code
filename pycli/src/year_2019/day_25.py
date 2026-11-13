import re
import threading
from collections import defaultdict

from pycli.src.year_2019.intcode import QueueIntCodeComputer
from pydantic import BaseModel, ConfigDict, Field


room_description_pattern = re.compile(
    r"\A== (?P<room>.+?) ==\n"
    r"(?P<description>.*?)(?=\n\nDoors here lead:)"
    r"\n\nDoors here lead:\n"
    r"(?P<directions>(?:- [^\n]*\n?)+)"
    r"(?:\nItems here:\n(?P<items>(?:- [^\n]*\n?)+))?"
    r"(?:\nCommand\?)?\Z",
    re.DOTALL,
)

inventory_pattern = re.compile(
    r"\AItems in your inventory:\n"
    r"(?P<items>(?:- [^\n]+\n?)+)"
    r"\nCommand\?\s*\Z"
)

SIZE = 40


class Room(BaseModel):
    name: str
    description: str = Field(repr=False)
    available_directions: frozenset[str] = Field(repr=False)
    model_config = ConfigDict(frozen=True)


class Computer(QueueIntCodeComputer):
    idle: threading.Event = threading.Event()
    values: list = []

    def put(self, value):
        if value == 10:
            self.idle.clear()
        super().put(value)

    def output(self, item):
        self.values.append(item)
        if tuple(self.values[-8:]) in {
            (67, 111, 109, 109, 97, 110, 100, 63),
            (114, 108, 111, 99, 107, 46, 34, 10),
        }:
            super().output("".join(chr(char) for char in self.values).strip())
            self.values = []


REVERSED_DIRECTIONS = {
    "south": "north",
    "north": "south",
    "east": "west",
    "west": "east",
}

PRESSURE_CHECKPOINT = "Security Checkpoint"
PRESSURE_DIRECTION = "south"


class PasswordFound(Exception):
    pass


class Game:
    def __init__(self, computer):
        thread = threading.Thread(target=computer.run)
        thread.start()
        self.computer = computer
        self.current_room = None
        self.rooms = set()
        self.inventory = set()
        self.item_by_room = defaultdict(set)
        self.visited = set()
        self.neighbours = defaultdict(set)

        desc = self.computer.get()
        self.explore_room(desc)

    def _instruct(self, instruction):
        for char in map(ord, instruction):
            self.computer.put(char)
        self.computer.put(10)
        return self.computer.get()

    def instruct(self, instruction, display=True):

        text = self._instruct(instruction)
        if display:
            print(f">  {instruction}")
            print(text)

        match instruction.split():
            case ["north" | "south" | "east" | "west"]:
                self.move(instruction, text)

            case ["take", *item]:
                self.take(" ".join(item), text)

            case ["drop", *item]:
                self.drop(" ".join(item), text)

            case ["inv"]:
                self.get_inventory(text)

            case _:
                raise ValueError(instruction)

        # self.print_map()

    def get_inventory(self, text):
        items = self.parse_get_inventory(text)
        assert self.inventory == items, (self.inventory, items)

    def parse_get_inventory(self, text):
        if "You aren't carrying any items." in text:
            return []

        match = inventory_pattern.fullmatch(text)
        assert match is not None, repr(text)
        return {line.removeprefix("- ").strip() for line in match["items"].splitlines()}

    def take(self, item, text):
        parsed = self.parse_take(text)
        assert item == parsed, (item, parsed)
        self.inventory.add(item)
        self.item_by_room[self.current_room].remove(item)

    def parse_take(self, text):
        return text.removeprefix("You take the ").removesuffix(".\n\nCommand?")

    def drop(self, item, text):
        parsed = self.parse_drop(text)
        assert item == parsed, (item, parsed)
        self.inventory.remove(item)
        self.item_by_room[self.current_room].add(item)

    def parse_drop(self, text):
        return text.removeprefix("You drop the ").removesuffix(".\n\nCommand?")

    def move(self, instruction, text):
        if text == "You can't go that way.\n\nCommand?":
            return

        if "Analyzing..." in text:
            self.visited.add("Pressure-Sensitive Floor")
            return

        self.explore_room(text)

    def explore_room(self, text):
        parsed = self.parse_move(text)

        self.current_room = Room(
            name=parsed["room"],
            description=parsed["description"],
            available_directions=frozenset(parsed["directions"]),
        )
        self.rooms.add(self.current_room)

        if self.current_room not in self.visited:
            for item in parsed["items"]:
                self.item_by_room[self.current_room].add(item)

            self.visited.add(self.current_room)

    def parse_move(self, description):
        match = room_description_pattern.fullmatch(description)
        assert match is not None, repr(description)
        return {
            "room": match["room"],
            "description": match["description"].strip(),
            "directions": [
                line.removeprefix("- ").strip()
                for line in match["directions"].splitlines()
            ],
            "items": [
                line.removeprefix("- ").strip()
                for line in (match["items"] or "").splitlines()
            ],
        }

    def explore(self, room, path=()):
        while allowed_items := self.item_by_room[self.current_room] - {
            "photons",
            "giant electromagnet",
            "infinite loop",
            "molten lava",
            "escape pod",
        }:
            self.instruct(f"take {next(iter(allowed_items))}", display=False)

        for direction in room.available_directions:
            if room.name == PRESSURE_CHECKPOINT and direction == PRESSURE_DIRECTION:
                self.pressure_path = path
                continue

            previous_room = self.current_room
            visited_before = self.visited.copy()

            self.instruct(direction, display=False)

            if self.current_room is previous_room:
                continue

            next_room = self.current_room

            if next_room not in visited_before:
                self.explore(next_room, path + (direction,))

            self.instruct(REVERSED_DIRECTIONS[direction], display=False)

    def pass_pressure_sensor(self):
        items = sorted(self.inventory)
        for item in items:
            self.instruct(f"drop {item}", display=False)

        def backtrack(options, current):
            description = self._instruct("south")

            if description.startswith(
                '== Pressure-Sensitive Floor ==\nAnalyzing...\n\nDoors here lead:\n- north\n\nA loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.'
            ):
                return

            elif not description.startswith(
                '== Pressure-Sensitive Floor ==\nAnalyzing...\n\nDoors here lead:\n- north\n\nA loud, robotic voice says "Alert! Droids on this ship are heavier than the detected value!" and you are ejected back to the checkpoint.'
            ):
                return int(re.search(r"\d+", description).group())

            remaining = options.copy()

            for item in options:
                remaining.pop(0)

                current.append(item)
                self.instruct(f"take {item}", display=False)
                result = backtrack(remaining, current)
                if result is not None:
                    return result

                self.instruct(f"drop {item}", display=False)
                current.pop()

        return backtrack(list(items), [])


def part_1(text, example: bool = False):
    computer = Computer.from_text(text)
    game = Game(computer)
    game.explore(game.current_room)
    for direction in game.pressure_path:
        game.instruct(direction, display=False)

    return game.pass_pressure_sensor()


def part_2(text, example: bool = False):
    result = None
    return result
