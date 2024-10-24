import re
from collections import defaultdict

from pycli.src.held_karp import shortest_hamiltionan_path


pattern = re.compile(r"(?P<start>\w+) to (?P<stop>\w+) = (?P<dist>\d+)")


def build_mapping(lines):
    distances = defaultdict(dict)
    for line in lines:
        start, stop, dist = pattern.match(line).groups()
        distances[start][stop] = int(dist)
        distances[stop][start] = int(dist)
    return distances


def build_matrix(distances):
    cities = {city: idx for idx, city in enumerate(distances)}
    N = len(cities)
    dists = [[0] * N for _ in range(N)]
    for city, _distances in distances.items():
        for other, distance in _distances.items():
            dists[cities[city]][cities[other]] = distance

    for i in range(N):
        for j in range(i + 1, N):
            assert dists[i][j] == dists[j][i] != 0
    return dists


def part_1(text, example: bool = False):
    lines = text.strip().split("\n")
    distances = build_mapping(lines)
    distance_matrix = build_matrix(distances)
    result, _ = shortest_hamiltionan_path(distance_matrix)
    return result


def part_2(text, example: bool = False):
    lines = text.strip().split("\n")
    distances = build_mapping(lines)
    distance_matrix = build_matrix(distances)
    result, _ = shortest_hamiltionan_path(distance_matrix, max_value=True)
    return result
