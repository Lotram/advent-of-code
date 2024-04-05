import re
from itertools import batched, count

from pydantic import BaseModel


def part_1(text, example=False):
    result = None
    print(result)


class Range(BaseModel):
    destination: int
    source: int
    length: int


class Map(BaseModel):
    ranges: list[Range]

    def get_previous_value(self, value: int):
        for range_ in self.ranges:
            if range_.destination <= value < range_.destination + range_.length:
                return range_.source + value - range_.destination
        return value


class SeedRange(BaseModel):
    start: int
    length: int

    @classmethod
    def from_tuple(cls, t) -> "SeedRange":
        return cls(start=t[0], length=t[1])

    def has_value(self, value: int):
        return self.start <= value < self.start + self.length


class Maps(BaseModel):
    maps: list[Map]
    seeds: list[SeedRange]

    def has_seed(self, value):
        for map_ in self.maps:
            value = map_.get_previous_value(value)

        for seed in self.seeds:
            if seed.has_value(value):
                return True
        return False


def build_maps(lines):
    maps = []
    ranges = []
    for line in lines:
        if line[0].isdigit():
            destination, source, length = map(int, line.split())
            ranges.append(Range(destination=destination, source=source, length=length))
        else:
            if ranges:
                maps.append(Map(ranges=ranges))
                ranges = []
    maps.append(Map(ranges=ranges))
    return maps


def part_2(text, example=False):
    lines = text.strip().split("\n")
    result = None
    seeds = list(map(SeedRange.from_tuple, batched(re.findall(r"\d+", lines[0]), 2)))
    map_list = build_maps(lines[1:])
    maps = Maps(maps=map_list[::-1], seeds=seeds)
    counter = count()
    while True:
        value = next(counter)
        if maps.has_seed(value):
            result = value
            break

    return result
