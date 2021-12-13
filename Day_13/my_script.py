from pathlib import Path
import numpy as np
import re

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_13" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_13" / "example_input.txt"


def get_input(filepath: Path) -> tuple[list[tuple], list[tuple]]:
    coordinates = []
    commands = []
    with open(filepath, "r") as f:
        content = f.read()
        coordinates_raw, commands_raw = content.split("\n\n")

        for number in coordinates_raw.split("\n"):
            coordinates.append(tuple(map(int, number.split(","))))  # [(x, y), (x, y), ...]
        
        for command in commands_raw.split("\n"):
            part1 = re.search('\w=', command)  # Find the command
            part2 = re.search('\d+', command)  # Find the number
            commands.append((part1.group(0)[0], int(part2.group(0))))  # [('x', 1), ('y', 2)]
            
    return coordinates, commands


def build_map(coordinates: list[tuple]) -> np.array:
    rows = 0
    columns = 0
    for x, y in coordinates:
        if x > columns:
            columns = x
        if y > rows:
            rows = y

    map = np.zeros((rows + 1, columns + 1), dtype=int)
    
    for x, y in coordinates:
        map[y][x] = 1

    return map


def fold_map(map: np.array, command: tuple) -> np.array:
    if command[0] == 'x':
        return fold_x(map, command[1])
    elif command[0] == 'y':
        return fold_y(map, command[1])
    else:
        return map


def fold_x(map: np.array, x: int) -> np.array:
    # fold vertically
    n_columns = len(map[0])
    n_columns_to_fold = n_columns - x

    for i in range(n_columns_to_fold):
        map[:, x - i] = map[:, x - i] | map[:, x + i]

    return np.delete(map, slice(x, n_columns), axis=1)


def fold_y(map: np.array, y: int) -> np.array:
    # fold horizontally
    n_rows = len(map)
    n_rows_to_fold = n_rows - y

    for i in range(n_rows_to_fold):
        map[y - i] = map[y - i] | map[y + i]

    return np.delete(map, slice(y, n_rows), axis=0)


def print_map(map: np.array):
    for row in map:
        print("".join(['#' if i == 1 else '.' for i in list(row)]))


def part_1(coordinates: list[tuple], commands: list[tuple]) -> int:
    # 1. build map
    map = build_map(coordinates)
    # print(map)

    # 2. fold map only once
    map = fold_map(map, commands[0])
    # print(commands[0])
    # print(map)

    # 3. count elements
    return sum(sum(row) for row in map)


def part_2(coordinates: list[tuple], commands: list[tuple]) -> int:
    # 1. build map
    map = build_map(coordinates)
    # print(map)

    # 2. fold map
    for command in commands:
        map = fold_map(map, command)
        # print(command)
        # print(map)

    # 3. read code
    print_map(map)


if __name__ == '__main__':
    # horizontal position of each crab
    # -> make all of their horizontal positions match while requiring them to spend as little fuel as possible
    print(INPUT_FILE)

    # parse input 
    example_coordinates, example_commands = get_input(EXAMPLE_INPUT_FILE)
    print(example_coordinates)
    print(example_commands)

    coordinates, commands = get_input(INPUT_FILE)
    print(len(coordinates))
    print(len(commands))

    # Part 1
    print(part_1(example_coordinates, example_commands)) 
    print(part_1(coordinates, commands))
    
    # Part 2
    part_2(example_coordinates, example_commands)
    part_2(coordinates, commands)  # FPEKBEJL