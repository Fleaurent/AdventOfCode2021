from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_1" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_1" / "example_input.txt"


def get_input(filepath: Path) -> list:
    data = []

    with open(filepath, "r") as f:
        lines = f.readlines()
        data = [int(i) for i in lines]

    return data


def depth_increase(data: list) -> int:
    n_depth_increased = 0

    for i in range(len(data) - 1):
        if data[i] < data[i+1]:
            n_depth_increased += 1
    
    return n_depth_increased


def depth_increase_sliding_window(data: list) -> int:
    n_depth_increased = 0

    for i in range(len(data) - 3):
        sliding_window_1 = data[i] + data[i+1] + data[i+2]
        sliding_window_2 = data[i+1] + data[i+2] + data[i+3]

        if sliding_window_1 < sliding_window_2:
            n_depth_increased += 1

    return n_depth_increased


if __name__ == '__main__':
    print(INPUT_FILE)

    example_data = get_input(EXAMPLE_INPUT_FILE)
    print(example_data)

    data = get_input(INPUT_FILE)
    print(len(data))

    # Part 1
    print(depth_increase(example_data))
    print(depth_increase(data))

    # Part 2
    print(depth_increase_sliding_window(example_data))
    print(depth_increase_sliding_window(data))
