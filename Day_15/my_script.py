from pathlib import Path
import numpy as np
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_15" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_15" / "example_input.txt"


def get_input(filepath: Path) -> list[list[int]]:
    map = []

    with open(filepath, "r") as f:
        for line in f.readlines():
            map.append([int(x) for x in line.strip()])
            
    return np.array(map)


def calculate_warp_path_cost_matrix(map: list[list[int]]) -> np.array:
    """Compute accumulated cost matrix for warp path 
    """
    distances = np.array(map)
    n_rows, n_cols = distances.shape

    # Initialization
    cost = np.zeros((n_rows, n_cols)).astype(int)
    cost[0,0] = distances[0,0]
    
    # init first column: sum up
    for i in range(1, n_rows):
        cost[i, 0] = distances[i, 0] + cost[i-1, 0]  
    
    # init first row: sum up
    for j in range(1, n_cols):
        cost[0, j] = distances[0, j] + cost[0, j-1]  

    # Accumulated warp path cost
    for i in range(1, n_rows):
        for j in range(1, n_cols):
            cost[i, j] = min(
                cost[i-1, j],    # insertion
                cost[i, j-1],    # deletion
            ) + distances[i, j] 
    
    return cost - cost[0, 0]


def part_1(map: list[list[int]]) -> int:
    cost_matrix = calculate_warp_path_cost_matrix(map)
    print(cost_matrix)    
    return cost_matrix[-1, -1]


def build_large_map(map: list[list[int]]) -> list[list[int]]:
    # increase map size by 1
    n_rows, n_cols = map.shape
    large_map = np.zeros((n_rows*5, n_cols*5)).astype(int)

    for map_tile_row in range(5):
        for map_tile_col in range(5):
            large_map[map_tile_row*n_rows:(map_tile_row+1)*n_rows, map_tile_col*n_cols:(map_tile_col+1)*n_cols] = increment_map(map, map_tile_row+map_tile_col)
    return large_map


def increment_map(map: list[list[int]], num: int) -> list[list[int]]:
    for _ in range(num):
        map = (map + 1) % 10
        map[map == 0] = 1

    return map

def part_2(map: list[list[int]]) -> int:
    large_map = build_large_map(map)
    print(large_map)
    np.savetxt("large_map.csv", large_map, fmt='%d', delimiter=",")
    large_cost_matrix = calculate_warp_path_cost_matrix(large_map)
    print(large_cost_matrix)
    np.savetxt("large_cost_matrix.csv", large_cost_matrix, fmt='%04d', delimiter=",")
    return large_cost_matrix[-1, -1]


if __name__ == '__main__':
    print(INPUT_FILE)

    # parse input 
    example_map = get_input(EXAMPLE_INPUT_FILE)
    print(example_map)

    map = get_input(INPUT_FILE)
    print(len(map))
    print(len(map[0]))

    # Part 1
    print(part_1(example_map)) 
    print(part_1(map))
    
    # Part 2
    print(part_2(example_map)) 
    print(part_2(map))
