from collections.abc import Iterable
from itertools import count
from typing import Literal

import numpy as np
from pycli.src.dijkstra import matrix_dijkstra
from pycli.src.grid import DIRECTIONS, EAST, NORTH, SOUTH, WEST, Grid, Vector
from pydantic import BaseModel


class Unit(BaseModel):
    idx: int
    type: Literal["E"] | Literal["G"]
    hit_points: int = 200
    attack: int = 3

    def __hash__(self):
        return hash((self.type, self.idx))


class Elf(Unit):
    type: Literal["E"] = "E"


class Goblin(Unit):
    type: Literal["G"] = "G"


class CombatOver(Exception):
    pass


class ElfDied(Exception):
    pass


class Map:
    def __init__(self, grid, positions, part=1):
        self.grid = grid
        self.positions = positions
        self.part = part

    def is_reachable(self, position):
        return (
            position in self.grid
            and self.grid[position] == "."
            and position not in self.positions
        )

    def print(self):
        lines = [[] for _ in range(self.grid.row_size)]
        for position, char in self.positions.items():
            self.grid[position] = char.type
            lines[int(position[0])].append(f"{char.type}({char.hit_points})")

        self.grid.print()
        self.grid.replace("E", ".")
        self.grid.replace("G", ".")

        print()
        for line in lines:
            if line:
                print(", ".join(line))
        print()

    def neighbour_func(self, grid, position: Vector) -> Iterable[tuple[Vector, int]]:
        for direction in (NORTH, WEST, EAST, SOUTH):
            _position = direction + position
            if self.is_reachable(_position):
                yield (_position, 1)

    # FIXME: this takes way too much time
    def move(self, position, enemies):
        targets = {
            target
            for pos in enemies
            for direction in DIRECTIONS
            if self.is_reachable(target := pos + direction)
        }
        if not targets:
            return None

        if position in targets:
            return position

        # Find the target square
        target, (dist, path) = min(
            (
                (
                    target,
                    matrix_dijkstra(self.grid, position, target, self.neighbour_func),
                )
                for target in targets
            ),
            key=lambda item: (item[1][0], item[0]),
        )

        if dist == float("inf"):
            return None

        # Find the next position
        dist, start = min(
            (
                matrix_dijkstra(self.grid, start, target, self.neighbour_func)[0],
                start,
            )
            for direction in DIRECTIONS
            if self.is_reachable(start := position + direction)
        )

        return start

    def attack(self, position, char, enemies):
        reachable_enemies = [
            (_pos, enemy)
            for _pos, enemy in enemies.items()
            if (position - _pos).norm() <= 1
        ]
        if not reachable_enemies:
            return

        (enemy_pos, enemy) = min(
            reachable_enemies,
            key=lambda item: (item[1].hit_points, item[0]),
        )
        enemy.hit_points -= char.attack
        if enemy.hit_points <= 0:
            if self.part == 2 and enemy.type == "E":
                raise ElfDied()
            del self.positions[enemy_pos]

    def run_turn(self, char_position):
        char = self.positions.pop(char_position, None)
        if char is None:  # char is dead
            return

        enemies = {
            _pos: _char
            for _pos, _char in self.positions.items()
            if _char.type != char.type
        }
        if not enemies:
            self.positions[char_position] = char
            raise CombatOver()

        next_position = self.move(char_position, enemies)
        self.positions[next_position or char_position] = char

        if next_position is None:
            return

        self.attack(next_position, char, enemies)

    def run_round(self):
        for char_position, char in sorted(self.positions.items()):
            if char.hit_points > 0:
                self.run_turn(char_position)

    def run(self):
        round_counter = 0
        try:
            while True:
                self.run_round()
                round_counter += 1
        except CombatOver:
            print(f"finished after {round_counter} rounds")
            self.print()
            print()
            return (
                sum(char.hit_points for char in self.positions.values()) * round_counter
            )


def parse_grid(text) -> Grid:
    return Grid(np.array(list(map(list, text.rstrip("\n").split("\n")))))


def solve(text, elf_attack=3, part=1):
    grid = parse_grid(text)
    elfs = {
        position: Elf(idx=idx, attack=elf_attack)
        for idx, position in enumerate(grid.find_all("E"))
    }
    goblins = {
        position: Goblin(idx=idx) for idx, position in enumerate(grid.find_all("G"))
    }
    grid.replace("E", ".")
    grid.replace("G", ".")

    map_ = Map(grid, elfs | goblins, part)
    result = map_.run()
    return result


def part_1(text, example: bool = False):
    return solve(text)


def part_2(text, example: bool = False):
    for elf_attack in count(4):
        print(elf_attack)
        try:
            result = solve(text, elf_attack, 2)
        except ElfDied:
            continue
        else:
            print(elf_attack)
            return result
