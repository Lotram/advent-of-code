from pydantic import BaseModel, Field, model_validator


class Node(BaseModel):
    id: int = Field(frozen=True)
    start: int
    end: int
    weight: int

    @model_validator(mode="before")
    @classmethod
    def compute_weight(cls, data):
        if data.get("weight") is None:
            data["weight"] = int(data["start"]) + int(data["end"])
        return data

    def get_other_end(self, value):
        match value:
            case self.start:
                return self.end

            case self.end:
                return self.start

            case _:
                raise ValueError(f"{value} not in node")

    def __hash__(self):
        return hash(self.id)


def merge(a, b, value):
    return Node(
        id=a.id,
        start=a.get_other_end(value),
        end=b.get_other_end(value),
        weight=a.weight + b.weight,
    )


# FIXME there is a problem in this function
def simplify(nodes):
    values = sorted(
        ({node.start for node in nodes} | {node.end for node in nodes}) - {0}
    )
    for value in values:
        doubles = {node for node in nodes if (node.start, node.end) == (value, value)}
        assert len(doubles) <= 1
        nodes -= doubles
        _nodes = {
            node
            for node in nodes
            if value in {node.start, node.end} and node.start != node.end
        }

        if doubles:
            for _node in _nodes:
                _node.weight += value
        if len(_nodes) == 2:
            new = merge(*_nodes, value)
            nodes -= _nodes
            nodes.add(new)

    return nodes


def get_max(current_value, available, score):
    candidates = {node for node in available if current_value in {node.start, node.end}}
    if candidates:
        return max(
            get_max(
                node.get_other_end(current_value),
                available - {node},
                score + node.weight,
            )
            for node in candidates
        )
    else:
        return score


def part_1(text, example: bool = False):

    nodes = {
        Node(id=idx, start=start, end=end)
        for idx, (start, end) in enumerate(
            line.split("/") for line in text.strip().split("\n")
        )
    }
    # this is broken
    # simplify(nodes)

    result = get_max(0, nodes, 0)
    return result


def get_longest(current_value, available, length, score):
    candidates = {node for node in available if current_value in {node.start, node.end}}
    if candidates:
        return max(
            get_longest(
                node.get_other_end(current_value),
                available - {node},
                length + 1,
                score + node.weight,
            )
            for node in candidates
        )
    else:
        return (length, score)


def part_2(text, example: bool = False):
    nodes = {
        Node(id=idx, start=start, end=end)
        for idx, (start, end) in enumerate(
            line.split("/") for line in text.strip().split("\n")
        )
    }
    # this is broken
    # simplify(nodes)

    result = get_longest(0, nodes, 0, 0)
    return result[1]
