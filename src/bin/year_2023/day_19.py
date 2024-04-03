import re
from operator import gt, lt
from typing import NamedTuple

from pydantic import BaseModel


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


class Condition(BaseModel):
    part: str
    operator: str
    value: int

    def process(self, part):
        attr = getattr(part, self.part)
        op = lt if self.operator == "<" else gt
        return op(attr, self.value)

    def split(self, range):
        other_attrs = {
            part: getattr(range, part)
            for part in {"target", "x", "m", "a", "s"} - {self.part}
        }
        value = getattr(range, self.part)
        lower = (value[0], min(value[1], self.value - (self.operator == "<")))
        upper = (max(value[0], lower[1] + 1), value[1])
        range_1 = Range(**{**other_attrs, **{self.part: lower}})
        range_2 = Range(**{**other_attrs, **{self.part: upper}})

        return [r for r in (range_1, range_2) if r.len()]


class Rule(BaseModel):
    condition: Condition | None = None
    target: str

    def process(self, part):
        if self.condition is None or self.condition.process(part):
            return self.target

    def split(self, range):
        if not self.condition:
            range.target = self.target
            return [range]

        cond = self.condition

        other_attrs = {
            part: getattr(range, part)
            for part in {"target", "x", "m", "a", "s"} - {cond.part}
        }
        value = getattr(range, cond.part)
        lower = (value[0], min(value[1], cond.value - (cond.operator == "<")))
        upper = (max(value[0], lower[1] + 1), value[1])
        range_1 = Range(
            **{
                **other_attrs,
                **{
                    cond.part: lower,
                    "target": self.target if cond.operator == "<" else range.target,
                },
            }
        )
        range_2 = Range(
            **{
                **other_attrs,
                **{
                    cond.part: upper,
                    "target": self.target if cond.operator == ">" else range.target,
                },
            }
        )

        return [r for r in (range_1, range_2) if r.len()]


class Workflow(BaseModel):
    name: str
    rules: list[Rule]

    def process(self, part):
        for rule in self.rules:
            if target := rule.process(part):
                return target


workflow_pattern = re.compile(
    r"(?:(?P<part>x|m|a|s)(?P<operator><|>)(?P<value>\d+):)?(?P<target>\w+)"
)

part_pattern = re.compile(r"{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}")


def parse_workflow(workflow):
    name, conditions = workflow[:-1].split("{")
    rules = []
    for cond in conditions.split(","):
        part, operator, value, target = workflow_pattern.match(cond).groups()

        if part:
            condition = Condition(part=part, operator=operator, value=value)
        else:
            condition = None
        rules.append(Rule(condition=condition, target=target))

    return Workflow(name=name, rules=rules)


def parse_part(part):
    return Part(*tuple(map(int, part_pattern.match(part).groups())))


def part_1(text, example: bool = False):
    workflows, parts = text.strip().split("\n\n")
    workflows = [parse_workflow(workflow) for workflow in workflows.split("\n")]
    workflows = {workflow.name: workflow for workflow in workflows}
    parts = [parse_part(part) for part in parts.split("\n")]

    accepted = []
    rejected = []

    for part in parts:
        workflow = workflows["in"]
        while True:
            target = workflow.process(part)
            if target == "A":
                accepted.append(part)
                break
            elif target == "R":
                rejected.append(part)
                break
            else:
                workflow = workflows[target]

    result = sum(sum(part) for part in accepted)
    return result


class Range(BaseModel):
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]
    target: str

    def len(self):
        return (
            max(self.x[1] - self.x[0] + 1, 0)
            * max(self.m[1] - self.m[0] + 1, 0)
            * max(self.a[1] - self.a[0] + 1, 0)
            * max(self.s[1] - self.s[0] + 1, 0)
        )


def part_2(text, example: bool = False):
    workflows, parts = text.strip().split("\n\n")
    workflows = [parse_workflow(workflow) for workflow in workflows.split("\n")]
    workflows = {workflow.name: workflow for workflow in workflows}

    q = [Range(x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000), target="in")]
    accepted = []
    rejected = []
    while q:
        range_ = q.pop(0)
        print(range_)
        while True:
            if range_ is None:
                break

            if range_.target == "A":
                accepted.append(range_)
                break
            elif range_.target == "R":
                rejected.append(range_)
                break

            workflow = workflows[range_.target]
            for rule in workflow.rules:
                ranges = rule.split(range_)
                for r in ranges:
                    if not r.target == workflow.name:
                        q.append(r)
                range_ = next((r for r in ranges if r.target == workflow.name), None)
                if range_ is None:
                    break

    result = sum(range_.len() for range_ in accepted)
    return result
