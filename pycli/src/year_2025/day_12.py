import re


region_pattern = r"\s*(?P<width>\d+)x(?P<height>\d+):\s*(?P<values>(?:\d+\s*)+)"


def parse_region(region):
    match = re.fullmatch(region_pattern, region)

    if not match:
        raise ValueError(f"Invalid line {region}")
    return (int(match.group("width")), int(match.group("height"))), [
        int(value) for value in match.group("values").split()
    ]


def part_1(text, example: bool = False):
    *shapes, regions = text.split("\n\n")
    sizes = [shape.count("#") for shape in shapes]

    regions = [parse_region(region) for region in regions.splitlines()]
    return sum(
        (width * length) >= sum(sizes[i] * count for i, count in enumerate(shape_count))
        for (width, length), shape_count in regions
    )


def part_2(text, example: bool = False):
    return None
