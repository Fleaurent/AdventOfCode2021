from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_6" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_6" / "example_input.txt"


def get_input(filepath: Path) -> list[int]:
    numbers = []

    with open(filepath, "r") as f:
        numbers = [int(number) for number in f.readline().strip().split(',')]

    return numbers


def part_1(numbers: list, n_days: int) -> int:
    # How many lanternfish would there be after 80 days
    # each lanternfish creates a new lanternfish once every 7 days
    # if new: set to 8
    # if overflow: reset to 6
    for day in range(n_days):
        # 1. reset day
        numbers = [number-1 for number in numbers]

        # 2. if day negative: count overflow + reset to 6
        n_spawns = sum(number < 0 for number in numbers)
        numbers = [6 if number < 0 else number for number in numbers]

        # 3. spawn new fish for every reset
        numbers += [8] * n_spawns

        # 4. check
        # print(f"{day+1}: {numbers}")

    return len(numbers)


def update_dict(numbers_dict: dict) -> dict:
    new_spawns = numbers_dict[0]
    old_numbers_dict = numbers_dict.copy()

    numbers_dict[0] = old_numbers_dict[1]
    numbers_dict[1] = old_numbers_dict[2]
    numbers_dict[2] = old_numbers_dict[3]
    numbers_dict[3] = old_numbers_dict[4]
    numbers_dict[4] = old_numbers_dict[5]
    numbers_dict[5] = old_numbers_dict[6]
    numbers_dict[6] = old_numbers_dict[7] + old_numbers_dict[0]
    numbers_dict[7] = old_numbers_dict[8]
    numbers_dict[8] = new_spawns
        
    return numbers_dict


def part_2(numbers: list, n_days: int) -> int:
    # dict approach
    # 1. init dict
    numbers_dict = {i: 0 for i in range(9)}

    # 2. parse day_0
    for number in numbers:
        numbers_dict[number] += 1

    # 3. update dict for each day
    for day in range(n_days):
        numbers_dict = update_dict(numbers_dict)

    # 4. count all fishes
    return sum(numbers_dict.values())


if __name__ == '__main__':
    print(INPUT_FILE)

    # parse input
    example_numbers = get_input(EXAMPLE_INPUT_FILE)
    print(example_numbers)

    numbers = get_input(INPUT_FILE)
    print(len(numbers))

    # # Part 1
    print(part_1(example_numbers, 80))  # 5934
    print(part_1(numbers, 80))

    # # Part 2
    print(part_2(example_numbers, 256))  # 26984457539
    print(part_2(numbers, 256))
