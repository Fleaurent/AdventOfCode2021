from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_14" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_14" / "example_input.txt"


def get_input(filepath: Path) -> tuple[str, dict[str, str]]:
    polymer_template = ""
    rules = {}

    with open(filepath, "r") as f:
        content = f.read()
        polymer_template, rules_raw = content.split("\n\n")

        for rule_raw in rules_raw.split("\n"):
            rules[rule_raw[:2]] = rule_raw[-1]
            
    return polymer_template, rules


def update_polymer(polymer: str, rules: dict[str, str]) -> str:
    new_polymer = ""
    for i in range(len(polymer) - 1):
        temp_chars = polymer[i:i+2]
        new_polymer += temp_chars[0]
        if(temp_chars in rules):
            new_polymer += rules[temp_chars]
    return new_polymer + polymer[-1]


def count_char_polymer(polymer: str) -> dict[str, int]:
    char_n = {}
    for char in set(polymer):
        n_char = polymer.count(char)
        char_n[char] = n_char

    return char_n

def find_min_max_char(char_n: dict[str, int]) -> tuple[int, int]: 
    max_char_n = 0
    min_char_n = sys.maxsize
    for char, char_n in char_n.items():
        if char_n > max_char_n:
            max_char_n = char_n
        if char_n < min_char_n:
            min_char_n = char_n
    
    return min_char_n, max_char_n


def part_1(polymer_template: str, rules: dict[str, str]) -> int:
    n_steps = 10
    polymer = polymer_template

    # update polymer
    for _ in range(n_steps):
        polymer = update_polymer(polymer, rules)

    # count characters in polymer
    char_n = count_char_polymer(polymer)

    # find smallest and largest char_n
    min_char_n, max_char_n = find_min_max_char(char_n)
    
    return max_char_n - min_char_n


def init_polymer_dict(polymer_template: str, rules: dict[str, str]) -> dict[str, int]:
    # 1. init
    polymer = {key: 0 for key in rules}

    # 2. count 
    for i in range(len(polymer_template) - 1):
        temp_chars = polymer_template[i:i+2]
        polymer[temp_chars] += 1

    return polymer


def update_polymer_dict(polymer: dict[str, int], rules: dict[str, str]) -> dict[str, int]:
    new_polymer = {key: 0 for key in rules}
    for key, count in polymer.items():
        if count > 0:
            # NN=1, NC=1, CB=1
            insert_key_1 = key[0] + rules[key]  # NC, NB, CH
            insert_key_2 = rules[key] + key[1]  # CN, BC, HB
            new_polymer[insert_key_1] += count 
            new_polymer[insert_key_2] += count 

    return new_polymer


def count_char_polymer_dict(polymer: dict[str, int], first_char: str, last_char: str) -> dict[str, int]:
    # count characters in polymer
    char_n = {}

    for key, count in polymer.items():
        for char_i in key:
            char_n[char_i] = char_n.get(char_i, 0) + count

    # correct character count
    for key, count in char_n.items():
        if key in [first_char, last_char]:
            char_n[key] = int((count+1) / 2)
        else:
            char_n[key] = int(count / 2)

    return char_n


def part_2(polymer_template: str, rules: dict[str, str]) -> int:
    n_steps = 40

    # 1. init polymer
    polymer = init_polymer_dict(polymer_template, rules)

    # 2. update polymer
    for _ in range(n_steps):
        polymer = update_polymer_dict(polymer, rules)

    # count characters in polymer
    first_char = polymer_template[0]
    last_char = polymer_template[-1]
    char_n = count_char_polymer_dict(polymer, first_char, last_char)

    # find smallest and largest char_n
    min_char_n, max_char_n = find_min_max_char(char_n)
    
    return max_char_n - min_char_n


if __name__ == '__main__':
    print(INPUT_FILE)

    # parse input 
    example_polymer_template, example_rules = get_input(EXAMPLE_INPUT_FILE)
    print(example_polymer_template)
    print(example_rules)

    polymer_template, rules = get_input(INPUT_FILE)
    print(len(polymer_template))
    print(len(rules))

    # Part 1
    print(part_1(example_polymer_template, example_rules)) 
    print(part_1(polymer_template, rules))
    
    # Part 2
    print(part_2(example_polymer_template, example_rules)) 
    print(part_2(polymer_template, rules))
    