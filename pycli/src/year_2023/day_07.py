from collections import Counter
from enum import IntEnum
from typing import ClassVar

from pydantic import BaseModel


class HandType(IntEnum):
    FIVE = 6
    FOUR = 5
    FULL_HOUSE = 4
    THREE = 3
    TWO_PAIRS = 2
    PAIR = 1
    HIGH = 0


class Hand(BaseModel):
    cards: str
    bidding: int
    card_order: ClassVar[str] = "AKQJT98765432"[::-1]

    def get_most_commons(self):
        return Counter(self.cards).most_common(2)

    def get_hand_type(self):
        most_commons = self.get_most_commons()

        match most_commons[0][1]:
            case 5:
                return HandType.FIVE
            case 4:
                return HandType.FOUR
            case 3:
                if most_commons[1][1] == 2:
                    return HandType.FULL_HOUSE
                else:
                    return HandType.THREE

            case 2:
                if most_commons[1][1] == 2:
                    return HandType.TWO_PAIRS
                else:
                    return HandType.PAIR

            case 1:
                return HandType.HIGH

            case _:
                raise ValueError(self.cards)

    def __lt__(self, other):
        if self.get_hand_type() != other.get_hand_type():
            return self.get_hand_type() < other.get_hand_type()
        else:
            for mine, other in zip(self.cards, other.cards, strict=False):
                if mine != other:
                    return self.card_order.index(mine) < self.card_order.index(other)


def part_1(text, example=False):
    lines = text.strip().split("\n")
    hands = []
    for line in lines:
        cards, bidding = line.split()
        hands.append(Hand(cards=cards, bidding=bidding))

    sorted_hands = sorted(hands)
    result = sum(idx * hand.bidding for idx, hand in enumerate(sorted_hands, 1))
    return result


class Hand2(Hand):
    card_order: ClassVar[str] = "AKQT98765432J"[::-1]

    def get_most_commons(self):
        most_commons = super().get_most_commons()
        if most_commons[0][0] == "J":
            if len(most_commons) > 1:
                most_commons = Counter(
                    self.cards.replace("J", most_commons[1][0])
                ).most_common(2)
        else:
            most_commons = Counter(
                self.cards.replace("J", most_commons[0][0])
            ).most_common(2)
        return most_commons


def part_2(text, example=False):
    lines = text.strip().split("\n")
    hands = []
    for line in lines:
        cards, bidding = line.split()
        hands.append(Hand2(cards=cards, bidding=bidding))

    sorted_hands = sorted(hands)
    result = sum(idx * hand.bidding for idx, hand in enumerate(sorted_hands, 1))
    return result
