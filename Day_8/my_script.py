"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

len(1)     = 2
len(7)     = 3
len(4)     = 4
len(2/3/5) = 5
len(0/6/9) = 6
len(8)     = 7

# a) parse simple numbers: 1, 4, 7, 8
parsed_numbers[1] = {c, f}
parsed_numbers[4] = {b, c, d, f}
parsed_numbers[7] = {a, c, f}
parsed_numbers[8] = {a, b, c, d, e, f, g}

# b) parse missing numbers: 0, 2, 3, 5, 6, 9
0 = {a, b, c, e, f, g} -> missing d
2 = {a, c, d, e, g}    -> missing b, f
3 = {a, c, d, f, g}    -> missing b, e 
5 = {a, b, d, f, g}    -> missing c, e
6 = {a, b, d, e, f, g} -> missing c
9 = {a, b, c, d, f, g} -> missing e

000
1 2
333
4 5
666

seven_segment = [
    # a b  c  d  e  f  g
    [1, 1, 1, 0, 1, 1, 1],  # 0
    [0, 0, 1, 0, 0, 1, 0],  # 1
    [1, 0, 1, 1, 1, 0, 1],  # 2
    [1, 0, 1, 1, 0, 1, 1],  # 3
    [0, 1, 1, 1, 0, 1, 0],  # 4
    [1, 1, 0, 1, 0, 1, 1],  # 5
    [1, 1, 0, 1, 1, 1, 1],  # 6
    [1, 0, 1, 0, 0, 1, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1],  # 8
    [1, 1, 1, 1, 0, 1, 1],  # 9
]
"""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_8" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_8" / "example_input.txt"

def get_input(filepath: Path) -> tuple[list[int], list[int]]:
    # Each entry consists of ten unique signal patterns, a | delimiter, and finally the four digit output value
    signals = []
    digits = []

    with open(filepath, "r") as f:
        for entry in f.readlines():
            entry_signals, entry_digit = entry.split(" | ")
            signals.append(entry_signals.split())
            digits.append(entry_digit.split())

    return signals, digits


def part_1(digits: list[int]) -> int:
    # how many times do digits 1, 4, 7, or 8 appear
    n_digits = 0

    for digit_entry in digits:
        for digit in digit_entry:
            match len(digit):
                case 2:
                    # found 1
                    n_digits += 1
                case 3:
                    # found 7
                    n_digits += 1
                case 4:
                    # found 4
                    n_digits += 1
                case 7:
                    # found 8
                    n_digits += 1

    return n_digits

def parse_numbers(numbers: list[str]) -> list[int]:
    segment_dict = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': []}
    parsed_numbers = [0 for i in range(10)]

    # 1. parse simple numbers
    numbers_len_5 = []
    numbers_len_6 = []
    for number in numbers:
        match len(number):
            case 2:
                # found 1
                parsed_numbers[1] = set(number)
            case 3:
                # found 7
                parsed_numbers[7] = set(number)
            case 4:
                # found 4
                parsed_numbers[4] = set(number)
            case 5:
                numbers_len_5.append(set(number))
            case 6:
                numbers_len_6.append(set(number))
            case 7:
                # found 8
                parsed_numbers[8] = set(number)
    
    # 2. parse segments
    b_d     = parsed_numbers[4] - parsed_numbers[1]
    e_g     = parsed_numbers[8] - parsed_numbers[7] - parsed_numbers[4]
    a_d_g   = numbers_len_5[0].intersection(*numbers_len_5)
    a_b_f_g = numbers_len_6[0].intersection(*numbers_len_6)

    segment_dict['a'] = list(parsed_numbers[7] - parsed_numbers[1])[0]
    segment_dict['g'] = list(e_g & a_d_g)[0]
    segment_dict['e'] = list(e_g - set(segment_dict['g']))[0]
    segment_dict['d'] = list(a_d_g - set(segment_dict['a']) - set(segment_dict['g']))[0]
    segment_dict['b'] = list(b_d - set(segment_dict['d']))[0]
    segment_dict['f'] = list(a_b_f_g - set(segment_dict['a']) - set(segment_dict['b']) - set(segment_dict['g']))[0]
    segment_dict['c'] = list(parsed_numbers[1] - set(segment_dict['f']))[0]

    # 3. parse remaining numbers
    """
    0 = {a, b, c, e, f, g} -> missing d
    2 = {a, c, d, e, g}    -> missing b, f
    3 = {a, c, d, f, g}    -> missing b, e 
    5 = {a, b, d, f, g}    -> missing c, e
    6 = {a, b, d, e, f, g} -> missing c
    9 = {a, b, c, d, f, g} -> missing e
    """
    parsed_numbers[0] = set(segment_dict['a'] + segment_dict['b'] + segment_dict['c'] + segment_dict['e'] + segment_dict['f'] + segment_dict['g'])
    parsed_numbers[2] = set(segment_dict['a'] + segment_dict['c'] + segment_dict['d'] + segment_dict['e'] + segment_dict['g'])
    parsed_numbers[3] = set(segment_dict['a'] + segment_dict['c'] + segment_dict['d'] + segment_dict['f'] + segment_dict['g'])
    parsed_numbers[5] = set(segment_dict['a'] + segment_dict['b'] + segment_dict['d'] + segment_dict['f'] + segment_dict['g'])
    parsed_numbers[6] = set(segment_dict['a'] + segment_dict['b'] + segment_dict['d'] + segment_dict['e'] + segment_dict['f'] + segment_dict['g'])
    parsed_numbers[9] = set(segment_dict['a'] + segment_dict['b'] + segment_dict['c'] + segment_dict['d'] + segment_dict['f'] + segment_dict['g'])        

    return parsed_numbers


def part_2(signals: list[int], digits: list[int]) -> int:
    sum_of_digits = 0
    for i in range(len(signals)):
        # parse 7 Segment order for each signal/digit combo
        numbers = signals[i] + digits[i]

        # 1. parse numbers
        parsed_numbers = parse_numbers(numbers)

        # 2. parse digits to values
        digit_numbers = [parsed_numbers.index(set(digit)) for digit in digits[i]]
        digit_number_i = int(''.join(map(str, digit_numbers)))
        sum_of_digits += digit_number_i

    return sum_of_digits


if __name__ == '__main__':
    # horizontal position of each crab
    # -> make all of their horizontal positions match while requiring them to spend as little fuel as possible
    print(INPUT_FILE)

    # parse input 
    example_signals, example_digits = get_input(EXAMPLE_INPUT_FILE)
    print(example_signals)
    print(example_digits)

    signals, digits = get_input(INPUT_FILE)
    print(len(signals))
    print(len(digits))

    # Part 1
    print(part_1(example_digits))
    print(part_1(digits))

    # Part 2
    print(part_2(example_signals, example_digits))
    print(part_2(signals, digits))
