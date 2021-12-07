from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_7" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_7" / "example_input.txt"


def get_input(filepath: Path) -> list[int]:
    numbers = []

    with open(filepath, "r") as f:
        numbers = [int(number) for number in f.read().strip().split(',')]

    return numbers


def part_1(numbers: list[int]) -> int:
    # 1. calculate median
    sorted_numbers = sorted(numbers)  # numbers.sort() == inplace
    median = sorted_numbers[int(len(numbers) / 2)]
    print(median)

    # 2. calculate fuel
    return sum(abs(number - median) for number in numbers)


# recursive bad idea: max recusion depth... -> use dict
def fuel_consumption_recursive(steps: int) -> int:
    if steps <= 1:
        return 1
    else:
        return fuel_consumption_recursive(steps-1) + steps   


def part_2(numbers: list[int]) -> int:
    largest_distance = max(numbers)

    # fuel consumption dict
    fuel_consumption = {0: 0}
    for i in range(1, largest_distance+1):
        fuel_consumption[i] = fuel_consumption[i-1] + i
    
    # calculate min fuel demand
    min_fuel_cost = sys.maxsize
    for i in range(largest_distance+1):
        i_fuel_cost = sum(fuel_consumption[abs(number - i)] for number in numbers)
        if i_fuel_cost < min_fuel_cost:
            min_fuel_cost = i_fuel_cost

    return min_fuel_cost


if __name__ == '__main__':
    # horizontal position of each crab
    # -> make all of their horizontal positions match while requiring them to spend as little fuel as possible
    print(INPUT_FILE)

    # parse input 
    example_numbers = get_input(EXAMPLE_INPUT_FILE)
    print(example_numbers)

    numbers = get_input(INPUT_FILE)
    print(len(numbers))

    # Part 1
    print(part_1(example_numbers))
    print(part_1(numbers))

    # Part 2
    # print([fuel_consumption_recursive(abs(i - 5)) for i in example_numbers])
    print(part_2(example_numbers))
    print(part_2(numbers))
