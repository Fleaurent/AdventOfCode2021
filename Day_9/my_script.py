from pathlib import Path
from functools import reduce
from operator import mul

import sys
from typing import no_type_check_decorator

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_9" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_9" / "example_input.txt"


def get_input(filepath: Path) -> list[list[int]]:
    heightmap = []
    with open(filepath, "r") as f:
        for entry in f.readlines():
            heightmap_row = [int(i) for i in entry.strip()]
            heightmap.append(heightmap_row)

    return heightmap


def is_low_point(heightmap: list[list[int]], row: int, col: int) -> bool:
    # heightmap[row][col] < max(up, down, left, right))
    n_rows = len(heightmap)
    n_cols = len(heightmap[0])

    if(row == 0):
        # check if corner
        if(col == 0):
            return heightmap[row][col] < min(heightmap[row+1][col], heightmap[row][col+1])
        elif(col == n_cols-1):
            return heightmap[row][col] < min(heightmap[row+1][col], heightmap[row][col-1])
        # first row: down, left, right
        return heightmap[row][col] < min(heightmap[row+1][col], heightmap[row][col-1], heightmap[row][col+1])
    elif(row == n_rows - 1):
        # check if corner
        if(col == 0):
            return heightmap[row][col] < min(heightmap[row-1][col], heightmap[row][col+1])
        elif(col == n_cols-1):
            return heightmap[row][col] < min(heightmap[row-1][col], heightmap[row][col-1])
        # last row: up, left, right
        return heightmap[row][col] < min(heightmap[row-1][col], heightmap[row][col-1], heightmap[row][col+1])
    elif(col == 0):
        # first column: up, down, right
        return heightmap[row][col] < min(heightmap[row-1][col], heightmap[row+1][col], heightmap[row][col+1])
    elif(col == n_cols - 1):
        # last column: up, down, left
        return heightmap[row][col] < min(heightmap[row-1][col], heightmap[row+1][col], heightmap[row][col-1])
    else:
        # normal case: up, down, left, right
        return heightmap[row][col] < min(heightmap[row-1][col], heightmap[row+1][col], heightmap[row][col-1], heightmap[row][col+1])

    return False


def get_low_points(heightmap: list[list[int]]) -> list[tuple]:
    n_rows = len(heightmap)
    n_cols = len(heightmap[0])
    low_points = []

    for row in range(n_rows):
        for col in range(n_cols):
            if(is_low_point(heightmap, row, col)):
                low_points.append((row, col))
                # print((row, col))
    return low_points


def part_1(heightmap: list[list[int]]) -> int:
    # 1. find low points: locations that are lower than any of its adjacent locations
    low_points = get_low_points(heightmap)
    
    # 2. sum of risk levels = low point + 1
    return sum(heightmap[row][col] + 1 for row, col in low_points)  # use generator not comprehension i.e. [... for ...  in ...]


def get_basin_size(heightmap: list[list[int]], low_point: tuple[int]) -> int:
    n_rows = len(heightmap)
    n_cols = len(heightmap[0])
    visited = set()
    basin_size = 0

    # 1. add neighbours to queue
    queue = [low_point]
    while(queue):
        # 1.1 pop from queue
        row, col = queue.pop(0)

        # 1.2 check if point is in heightmap
        if(row < 0 or row >= n_rows or col < 0 or col >= n_cols):
            continue

        # 1.3 check if point already visited
        if(visited.__contains__((row, col))):
            continue

        # 1.4 check that height is not 9
        height = heightmap[row][col]
        visited.add((row, col))
        
        # 1.5 append neighbours
        if(height != 9):
            # point belongs to basin
            basin_size += 1

            # add neighbours
            queue.append((row-1, col))  # up
            queue.append((row+1, col))  # down
            queue.append((row, col-1))  # right
            queue.append((row, col+1))  # left

    return basin_size


def part_2(heightmap: list[list[int]]) -> int:
    # 1. find low points: locations that are lower than any of its adjacent locations
    low_points = get_low_points(heightmap)

    # 2. find basin size for each low point
    basin_sizes = []
    for low_point in low_points:
        basin_size = get_basin_size(heightmap, low_point)
        basin_sizes.append(basin_size)

    # multiply together the sizes of the three largest basins
    return reduce(mul, sorted(basin_sizes)[-3:])  # mul == (lambda x, y: x * y)


if __name__ == '__main__':
    # horizontal position of each crab
    # -> make all of their horizontal positions match while requiring them to spend as little fuel as possible
    print(INPUT_FILE)

    # parse input 
    example_heightmap = get_input(EXAMPLE_INPUT_FILE)
    print(example_heightmap)

    heightmap = get_input(INPUT_FILE)
    print(len(heightmap))
    print(len(heightmap[0]))

    # Part 1
    print(part_1(example_heightmap))
    print(part_1(heightmap))

    # Part 2
    print(part_2(example_heightmap))
    print(part_2(heightmap))
