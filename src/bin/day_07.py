from collections import Counter
from enum import IntEnum

from pydantic import BaseModel

# card_order = "AKQJT98765432"[::-1]
card_order = "AKQT98765432J"[::-1]


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

    def get_hand_type(self):
        counter = Counter(self.cards)
        most_commons = counter.most_common(2)
        if most_commons[0][0] == "J":
            if len(most_commons) > 1:
                counter = Counter(self.cards.replace("J", most_commons[1][0]))
        else:
            counter = Counter(self.cards.replace("J", most_commons[0][0]))
        most_commons = counter.most_common(2)
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
            for mine, other in zip(self.cards, other.cards):
                if mine != other:
                    return card_order.index(mine) < card_order.index(other)


def part_1(lines):
    lines = lines.strip().split("\n")
    hands = []
    for line in lines:
        cards, bidding = line.split()
        hands.append(Hand(cards=cards, bidding=bidding))

    sorted_hands = sorted(hands)
    result = sum(idx * hand.bidding for idx, hand in enumerate(sorted_hands, 1))
    return result


def part_2(lines):
    lines = lines.strip().split("\n")
    hands = []
    for line in lines:
        cards, bidding = line.split()
        hands.append(Hand(cards=cards, bidding=bidding))

    sorted_hands = sorted(hands)
    result = sum(idx * hand.bidding for idx, hand in enumerate(sorted_hands, 1))
    return result
