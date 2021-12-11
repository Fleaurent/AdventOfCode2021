from pathlib import Path
import copy

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_11" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_11" / "example_input.txt"


def get_input(filepath: Path) -> list[list[int]]:
    grid = []
    with open(filepath, "r") as f:
        for grid_line in f.readlines():
            grid.append([int(i) for i in grid_line.strip()])

    return grid


def update_grid(grid: list[list[int]]) -> int:
    # update grid inplace
    n_rows    = len(grid)
    n_cols    = len(grid[0])
    flashed   = []  # An octopus can only flash at most once per step!

    # 1. increase every element in the grid
    for row_i in range(n_rows):
        for col_i in range(n_cols):
            if(row_i, col_i) not in flashed:
                grid[row_i][col_i] += 1
            else:
                grid[row_i][col_i] = 0


    while True:
        # 2. check elements that flashed
        flash_buffer = []
        for row_i in range(n_rows):
            for col_i in range(n_cols):
                if grid[row_i][col_i] > 9 and (row_i, col_i) not in flashed:
                    # flash
                    flash_buffer.append((row_i, col_i))
                    flashed.append((row_i, col_i))

        # 3. check if anything flashed
        if flash_buffer == []:
            return len(flashed)
        
        # 4. increase neighbors of flashed elements
        for row_i, col_i in flash_buffer:
            for row_j in range(row_i-1, row_i+2):
                for col_j in range(col_i-1, col_i+2):
                    if row_j >= 0 and row_j < n_rows and col_j >= 0 and col_j < n_cols:
                        if(row_j, col_j) not in flashed:
                            grid[row_j][col_j] += 1
                        else:
                            grid[row_j][col_j] = 0


def print_grid(grid: list[list[int]]):
    for row in grid:
        print(row)


def part_1(grid: list[list[int]]) -> int:
    temp_grid = copy.deepcopy(grid)

    total_flashes = 0
    for _ in range(100):
        flashes = update_grid(temp_grid)
        total_flashes += flashes

    return total_flashes


def part_2(grid: list[list[int]]) -> int:
    temp_grid = copy.deepcopy(grid)
    
    update_grid_step = 0
    while True:
        update_grid_step += 1
        flashes = update_grid(temp_grid)
        if flashes >= 100:
            return update_grid_step


if __name__ == '__main__':
    # horizontal position of each crab
    # -> make all of their horizontal positions match while requiring them to spend as little fuel as possible
    print(INPUT_FILE)

    # parse input 
    example_grid = get_input(EXAMPLE_INPUT_FILE)
    print_grid(example_grid)

    grid = get_input(INPUT_FILE)
    print_grid(grid)

    # Part 1
    print(part_1(example_grid))  # 1656
    print(part_1(grid))

    # Part 2
    print(part_2(example_grid))
    print(part_2(grid))
    