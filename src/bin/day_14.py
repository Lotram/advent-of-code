import re
from hashlib import md5
from itertools import count

THREE_CHARS = re.compile(r"(.)\1\1")
FIVE_CHARS = {char: re.compile(char * 5) for char in "0123456789abcdef"}


def get_hash(salt, index):
    return md5(salt + str(index).encode()).hexdigest()


def get_hash_2(salt, index):
    input_ = salt + str(index).encode()
    for _ in range(2017):
        input_ = md5(input_).hexdigest().encode()

    return input_.decode()


def build_class(salt, get_hash):
    class Hash:

        def __init__(self, idx):
            self.idx = idx
            self.digest = get_hash(salt, idx)
            triple_char = THREE_CHARS.search(self.digest)
            self.triple_char = triple_char.group()[0] if triple_char else None
            self.five_chars = {}

        def look_for_5(self, char):
            if char not in self.five_chars:
                if self.triple_char is None:
                    self.five_chars[char] = False
                else:
                    self.five_chars[char] = bool(FIVE_CHARS[char].search(self.digest))

            return self.five_chars[char]

    class Hashes:
        def __init__(self):
            self.hashes = {}

        def get(self, index):
            if index not in self.hashes:
                self.hashes[index] = Hash(idx=index)
            return self.hashes[index]

        def look_for_5(self, index, char):
            for idx in range(index + 1, index + 1001):
                hash = self.get(idx)
                if hash.look_for_5(char):
                    return True
            return False

    return Hashes()


def solution(salt, get_hash):
    hashes = build_class(salt, get_hash)

    results = []
    index_it = count()

    while len(results) < 64:
        hash = hashes.get(next(index_it))

        if hash.triple_char and hashes.look_for_5(hash.idx, hash.triple_char):
            results.append(hash.idx)

    result = results[-1]
    return result


def part_1(text):
    salt = text.strip().encode()
    return solution(salt, get_hash)


def part_2(text):
    salt = text.strip().encode()
    return solution(salt, get_hash_2)
