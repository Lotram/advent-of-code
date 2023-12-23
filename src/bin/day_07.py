from collections import defaultdict
from pathlib import Path


def build_tree(lines):
    assert lines[0] == "$ cd /"
    path = Path("/")

    tree = defaultdict(list)
    for line in lines:
        if line.startswith("$ cd"):
            path /= line.replace("$ cd", "").strip()
            path = path.resolve()
        elif line.startswith("$ ls") or line.startswith("dir"):
            continue
        else:
            size, _ = line.split(" ")
            tree[path].append(int(size))
            for parent in path.parents:
                tree[parent].append(int(size))

    return tree


def part_1(text):
    lines = text.strip().split("\n")
    tree = build_tree(lines)
    result = 0
    for value in tree.values():
        if sum(value) <= 100_000:
            result += sum(value)
    return result


def part_2(text):
    total_space = 70_000_000
    required_size = 30_000_000
    lines = text.strip().split("\n")
    tree = build_tree(lines)
    needed = required_size - (total_space - sum(tree[Path("/")]))
    return min(
        size for file_sizes in tree.values() if (size := sum(file_sizes)) >= needed
    )
