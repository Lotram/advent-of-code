def part_1(text):
    return sum(
        1
        for passphrase in text.strip().split("\n")
        if len(passphrase.split()) == len(set(passphrase.split()))
    )


def get_anagrams(words):
    return {"".join(sorted(word)) for word in words}


def part_2(text):
    return sum(
        1
        for passphrase in text.strip().split("\n")
        if len(passphrase.split()) == len(get_anagrams(passphrase.split()))
    )
