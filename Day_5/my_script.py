from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_5" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_5" / "example_input.txt"


def get_input(filepath: Path) -> list[list[tuple]]:
    line_coordinates = []

    with open(filepath, "r") as f:
        for line in f.readlines():
            p1, p2 = line.strip().split(" -> ")
            x1, y1 = p1.split(",")
            x2, y2 = p2.split(",")
            line_coordinates.append([(int(x1), int(y1)), (int(x2), int(y2))])

    return line_coordinates


def add_simple_line_to_grid(line: list[tuple], grid: list[list[int]]) -> list[list[int]]:
    # only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2
    [(x1, y1), (x2, y2)] = line
    
    if x1 == x2:
        # column line
        if y2 >= y1:
            # [(1, 1), (1, 3)]
            for y_i in range(y1, y2+1):
                grid[y_i][x1] += 1
        else:
            # [(1, 3), (1, 1)]
            for y_i in range(y1, y2-1, -1):
                grid[y_i][x1] += 1
    elif y1 == y2:
        # row line
        if x2 >= x1:
            # [(1, 3), (3, 3)]
            for x_i in range(x1, x2+1):
                grid[y1][x_i] += 1
        else:
            # [(3, 3), (1, 3)]
            for x_i in range(x1, x2-1, -1):
                grid[y1][x_i] += 1

    return grid


def add_line_to_grid(line: list[tuple], grid: list[list[int]]) -> list[list[int]]:
    # only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2
    [(x1, y1), (x2, y2)] = line
    
    if x1 == x2:
        # column line
        if y2 >= y1:
            # [(1, 1), (1, 3)]
            for y_i in range(y1, y2+1):
                grid[y_i][x1] += 1
        else:
            # [(1, 3), (1, 1)]
            for y_i in range(y1, y2-1, -1):
                grid[y_i][x1] += 1
    elif y1 == y2:
        # row line
        if x2 >= x1:
            # [(1, 3), (3, 3)]
            for x_i in range(x1, x2+1):
                grid[y1][x_i] += 1
        else:
            # [(3, 3), (1, 3)]
            for x_i in range(x1, x2-1, -1):
                grid[y1][x_i] += 1
    else:
        # diagonal line
        if x2 >= x1:
            xs = [x_i for x_i in range(x1, x2+1)]
        else:
            xs = [x_i for x_i in range(x1, x2-1, -1)]
    
        if y2 >= y1:
            ys = [y_i for y_i in range(y1, y2+1)]
        else:
            ys = [y_i for y_i in range(y1, y2-1, -1)]
        
        for x_i, y_i in zip(xs, ys):
            grid[y_i][x_i] += 1
                        
    return grid


def evaluate_grid(grid: list[list[int]]) -> int:
    # count number of points where at least two lines overlap
    points = 0

    for line in grid:
        for element in line:
            if element > 1:
                points += 1

    return points


def print_grid(grid: list[list[int]]):
    for row in grid:
        print(row)


def part_1(line_coordinates: list, grid_size: int) -> int:
    # init empty grid matrix: grid_size * grid_size
    grid = [[0 for j in range(grid_size)] for i in range(grid_size)]

    # add lines to the grid
    for line in line_coordinates:
        grid = add_simple_line_to_grid(line, grid)    
    
    # evaluate grid
    # print_grid(grid)
    return evaluate_grid(grid)


def part_2(line_coordinates: list, grid_size: int) -> int:
    # init empty grid matrix: grid_size * grid_size
    grid = [[0 for j in range(grid_size)] for i in range(grid_size)]

    # add lines to the grid
    for line in line_coordinates:
        grid = add_line_to_grid(line, grid)    
    
    # evaluate grid
    # print_grid(grid)
    return evaluate_grid(grid)


if __name__ == '__main__':
    print(INPUT_FILE)

    # parse input
    example_line_coordinates = get_input(EXAMPLE_INPUT_FILE)
    print(example_line_coordinates)

    line_coordinates = get_input(INPUT_FILE)
    print(len(line_coordinates)) 

    # Part 1
    print(part_1(example_line_coordinates, grid_size=10))
    print(part_1(line_coordinates, grid_size=1000))

    # Part 2
    print(part_2(example_line_coordinates, grid_size=10))
    print(part_2(line_coordinates, grid_size=1000))
