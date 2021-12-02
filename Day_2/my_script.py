from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_2" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_2" / "example_input.txt"


def get_input(filepath: Path) -> list:
    data = []

    with open(filepath, "r") as f:
        lines = f.readlines()

        for line in lines:
            direction, value = line.split()
            data.append([direction, int(value)])

    return data


def part_1(data: list) -> int:
    parsed_data = {}

    for direction, value in data:
        parsed_data[direction] = parsed_data.get(direction, 0) + value

    horizontal = parsed_data['forward'] 
    depth = parsed_data['down'] - parsed_data['up']
    return horizontal * depth


def part_2(data: list) -> int:
    aim = 0
    horizontal = 0
    depth = 0

    for direction, value in data:
        if direction == 'down':
            aim += value
        elif direction == 'up':
            aim -= value
        elif direction == 'forward':
            horizontal += value
            depth += aim * value

    return horizontal * depth


if __name__ == '__main__':
    print(INPUT_FILE)

    example_data = get_input(EXAMPLE_INPUT_FILE)
    print(example_data)

    data = get_input(INPUT_FILE)
    print(len(data))

    # Part 1
    print(part_1(example_data))
    print(part_1(data))

    # Part 2
    print(part_2(example_data))
    print(part_2(data))
