"""
#0: seti 123 0 2
#1: bani 2 456 2
#2: eqri 2 72 2
#3: addr 2 5 5
#4: seti 0 0 5
#5: seti 0 9 2

#6: bori 2 65536 1
#7: seti 1250634 6 2

#8: bani 1 255 4
#9: addr 2 4 2
#10: bani 2 16777215 2
#11: muli 2 65899 2
#12: bani 2 16777215 2
#13: gtir 256 1 4
#14: addr 4 5 5
#15: addi 5 1 5
#16: seti 27 2 5 | jump to 28


#17: seti 0 5 4 # b //= 256 and jump to #8
#18: addi 4 1 3
#19: muli 3 256 3
#20: gtrr 3 1 3
#21: addr 3 5 5
#22: addi 5 1 5
#23: seti 25 5 5 | jump to #26
#24: addi 4 1 4
#25: seti 17 2 5 | jump to #18
#26: setr 4 8 1
#27: seti 7 6 5

#28: eqrr 2 0 4 | halt if c == a else jump to #6
#29: addr 4 5 5
#30: seti 5 7 5
"""

Y = 1250634
Z = 65899


def solution(b):
    c = Y
    while True:
        c += b % 2**8
        c *= Z
        c %= 2**24
        if b < 2**8:
            return c
        b >>= 8


def part_1(text, example: bool = False):
    result = solution(2**16)
    return result


def part_2(text, example: bool = False):
    c = 0
    seen_values = set()
    prev = None
    while True:
        b = 2**16 | c
        c = solution(b)
        if c in seen_values:
            break
        seen_values.add(c)
        prev = c

    result = prev
    return result
