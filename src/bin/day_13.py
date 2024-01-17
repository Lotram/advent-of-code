import re
from collections import defaultdict

from .held_karp import held_karp_bitmask, shortest_hamiltionan_path

pattern = re.compile(
    r"(?P<start>\w+) would (?P<sign>gain|lose) (?P<value>\d+) happiness units by sitting next to (?P<stop>\w+)."
)


def build_mapping(lines):
    distances = defaultdict(dict)
    for line in lines:
        start, sign, value, stop = pattern.match(line).groups()
        distances[start][stop] = int(value) * (-1 if sign == "lose" else 1)
    return distances


def build_matrix(distances):
    cities = {city: idx for idx, city in enumerate(distances)}
    N = len(cities)
    dists = [[0] * N for _ in range(N)]
    for city, _distances in distances.items():
        for other, distance in _distances.items():
            dists[cities[city]][cities[other]] += distance
            dists[cities[other]][cities[city]] += distance

    return dists


def part_1(text):
    lines = text.strip().split("\n")
    distances = build_mapping(lines)
    distance_matrix = build_matrix(distances)
    result, _ = held_karp_bitmask(distance_matrix, max_value=True)
    return result


def part_2(text):
    lines = text.strip().split("\n")
    distances = build_mapping(lines)
    distance_matrix = build_matrix(distances)
    result, _ = shortest_hamiltionan_path(distance_matrix, max_value=True)
    return result
