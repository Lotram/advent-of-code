import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import batched, starmap

from .grid import Vector3D


@dataclass(slots=True)
class Particle:
    _position: Vector3D
    _speed: Vector3D
    acceleration: Vector3D

    def position(self, t):
        return self._position + t * self._speed + t * (t + 1) // 2 * self.acceleration

    def speed(self, t):
        self._speed + t * self.acceleration


pattern = re.compile(r"-?\d+")


def parse_line(line):
    return Particle(*starmap(Vector3D, batched(map(int, pattern.findall(line)), 3)))


def part_1(text, example: bool = False):
    particles = [parse_line(line) for line in text.strip().split("\n")]
    result, _ = min(
        ((idx, particle) for (idx, particle) in enumerate(particles)),
        key=lambda item: (
            item[1].acceleration.norm(),
            item[1]._speed.norm(),
            item[1]._position.norm(),
        ),
    )

    return result


def part_2(text, example: bool = False):
    particles = [parse_line(line) for line in text.strip().split("\n")]

    # empirical value
    for t in range(100):
        positions = defaultdict(list)
        for particle in particles:
            positions[tuple(particle.position(t))].append(particle)

        particles = [
            particles[0] for particles in positions.values() if len(particles) == 1
        ]

    return len(particles)
