import re
from functools import cached_property
from itertools import chain, combinations, count, product
from operator import and_, or_, xor


ops = {"OR": or_, "AND": and_, "XOR": xor}

pattern = re.compile(
    r"(?P<i1>[a-z0-9]{3}) (?P<op>XOR|OR|AND) (?P<i2>[a-z0-9]{3}) -> (?P<out>[a-z0-9]{3})"
)


class CycleError(Exception):
    pass


class InvalidGraph(Exception):
    pass


def parse(text):
    _inputs, wires = text.strip().split("\n\n")
    outputs = {}
    for _input in _inputs.splitlines():
        name, val = _input.split(": ")
        outputs[name] = {"inputs": (), "value": int(val)}

    for wire in wires.splitlines():
        match_ = pattern.match(wire)
        assert match_ is not None
        outputs[match_.group("out")] = {
            "op": ops[match_.group("op")],
            "inputs": (match_.group("i1"), match_.group("i2")),
            "value": None,
        }
    return outputs


class Solver:
    def __init__(self, text):
        self.graph = parse(text)
        self.swaps = set()
        self.visited = set()

    @cached_property
    def max_bit(self) -> int:
        for idx in count(0):
            if not (f"x{idx:0>2}" in self.graph and f"y{idx:0>2}" in self.graph):
                return idx - 1

        raise ValueError("max bit not found")

    def reset(self):
        self.visited = set()
        for name, data in self.graph.items():
            if name[0] not in "xy":
                data["value"] = None

    def swap(self, pair):
        self.swaps ^= {tuple(sorted(pair))}
        node_1, node_2 = pair
        new_inputs = {
            node_1: self.graph[node_2],
            node_2: self.graph[node_1],
        }
        self.graph[node_1] = {**new_inputs[node_1], "value": None}
        self.graph[node_2] = {**new_inputs[node_2], "value": None}

    def set_value(self, node):
        node_data = self.graph[node]
        if node_data["value"] is not None:
            return
        try:
            i1, i2 = node_data["inputs"]
            node_data["value"] = node_data["op"](self[i1], self[i2])

        except TypeError as err:
            raise CycleError from err

    def dfs(self, node, seen):
        self.visited.add(node)
        for neighbor in self.graph[node]["inputs"]:
            # if neighbor[0] in "yx" and int(neighbor[1:]) < idx - 1:
            #     print(node, neighbor, idx)
            seen.append(neighbor)
            if neighbor not in self.visited:
                self.dfs(neighbor, seen)

        self.set_value(node)

    def process(self, stop=None):
        self.reset()
        idx = 0
        seen_by_idx = []
        while (node := f"z{idx:0>2}") in self.graph:
            # if visited & {f"x{idx:0>2}", f"y{idx:0>2}"}:
            #     print(visited & {f"x{idx:0>2}", f"y{idx:0>2}"})

            seen = []
            self.dfs(node, seen)
            seen.append(node)
            seen_by_idx.append(seen)

            self.set_value(node)
            if stop and idx >= stop:
                break
            idx += 1

        return seen_by_idx

    def __getitem__(self, item: str | tuple[str, int]) -> int:
        if isinstance(item, tuple):
            item = f"{item[0]}{item[1]:0>2}"

        if item not in self.graph:
            raise ValueError(f"node not found {item}")

        return self.graph[item]["value"]

    def __setitem__(self, item: str | tuple[str, int], value: int):
        if isinstance(item, tuple):
            item = f"{item[0]}{item[1]:0>2}"

        if item not in self.graph:
            raise ValueError(f"node not found {item}")

        self.graph[item]["value"] = value

    def get_number(self, prefix) -> int:
        bits = self.max_bit + (prefix == "z")
        return sum(self[(prefix, bit)] * 2**bit for bit in range(bits + 1))

    def set_number(self, prefix, value):
        for bit in range(self.max_bit + 1):
            self[(prefix, bit)] = value % 2
            value >>= 1

    @property
    def x(self):
        return self.get_number("x")

    @x.setter
    def x(self, value):
        self.set_number("x", value)

    @property
    def y(self):
        return self.get_number("y")

    @y.setter
    def y(self, value):
        self.set_number("y", value)

    @property
    def z(self):
        return self.get_number("z")

    @z.setter
    def z(self, value):
        self.set_number("z", value)


def part_1(text, example: bool = False):
    solver = Solver(text)
    solver.process()
    result = solver.z

    return result


def find_problems(solver):
    failing_z_indexes = set()
    for bit in range(solver.max_bit):
        for x, y in product([0, 1], repeat=2):
            solver.x = x * 2**bit
            solver.y = y * 2**bit
            solver.process()

            if solver[("z", bit)] != (x ^ y):
                failing_z_indexes.add(bit)

            if solver[("z", bit + 1)] != (x & y):
                failing_z_indexes.add(bit + 1)

    group = set()
    groups = []
    for bit in sorted(failing_z_indexes):
        if group and not (group & {bit, bit - 1}):
            groups.append(group)
            group = set()

        group.add(bit)

    if group:
        groups.append(group)

    return groups


def try_swap(solver, swap, min_bit, max_bit):
    solver.swap(swap)
    assert solver.swaps == {tuple(sorted(swap))}
    for x, y in product(range(8), repeat=2):
        solver.reset()
        solver.x = x << (min_bit - 2)
        solver.y = y << (max_bit - 2)
        try:
            solver.process()
            if solver.z != (solver.x + solver.y):
                raise InvalidGraph
        except (CycleError, InvalidGraph):
            solver.swap(swap)
            assert not solver.swaps
            return False

    solver.swap(swap)
    return True


def fix_block(solver, seen_by_idx, failing_indexes):
    min_bit, max_bit = min(failing_indexes), max(failing_indexes)
    bits = list(range(min_bit, max_bit + 1))
    swaps = combinations(
        set(
            chain.from_iterable(
                sorted(node for node in seen_by_idx[bit] if node[0] not in "xy")
                for bit in bits
            )
        ),
        2,
    )
    valid_swaps = set()
    for swap in swaps:
        if try_swap(solver, swap, min_bit, max_bit):
            valid_swaps.add(swap)

    assert len(valid_swaps) == 1
    return valid_swaps.pop()


def part_2(text, example: bool = False):
    solver = Solver(text)
    seen_by_idx = solver.process()
    failing_index_groups = find_problems(solver)
    swaps = []
    for failing_indexes in failing_index_groups:
        swaps.extend(fix_block(solver, seen_by_idx, failing_indexes))

    result = ",".join(sorted(swaps))
    return result
