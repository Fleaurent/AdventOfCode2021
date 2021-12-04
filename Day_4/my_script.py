from pathlib import Path
import re

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_4" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_4" / "example_input.txt"


def get_input(filepath: Path) -> tuple[list, list]:
    numbers = []
    data = []

    with open(filepath, "r") as f:
        numbers = f.readline().strip().split(",")
        for line in f.readlines():
            if(line.strip()):
                data.append(line.strip())

    return numbers, data


def parse_boards(data: list) -> list:
    n_boards = int(len(data) / 5)
    boards = []

    for i in range(n_boards):
        # a)
        # temp_board = []
        # for j in range(5):
        #    temp_board.append(data[i*5 + j].split(" "))

        # b) simple split(None) -> on one or more whitespaces
        # temp_board = [data[i*5 + j].split() for j in range(5)]

        # c) regex " +" -> on one or more whitespaces
        temp_board = [re.split(" +", data[i*5 + j]) for j in range(5)]
        boards.append(temp_board)

    return boards


def numbers_on_board(numbers: list, board: list) -> bool:
    # board[rows, columns]
    # rows = board[:][i]
    # columns = board[i, :]
    
    n_rows = len(board)
    n_cols = len(board[0])

    numbers_set = set(numbers)
    
    # 1. check rows
    # set of numbers & set of row == row -> return yes
    for row in board:
        if(numbers_set & set(row) == set(row)):
            return True

    # 2. check columns
    # set of numbers & set of column == column -> return yes
    for i in range(n_cols):
        # column = board[i][:] # slicing only for numpy array
        column = [board[j][i] for j in range(n_rows)]

        if(numbers_set & set(column) == set(column)):
            return True    
    
    return False


def find_winner_board(numbers: list, boards: list) -> tuple[list, list]:
    # find and return winner_numbers and winner_board
    for i in range(5, len(numbers)):
        temp_numbers = numbers[:i]

        for board in boards:
            if(numbers_on_board(temp_numbers, board)):
                # return winner_numbers, winner_board
                return temp_numbers, board
    
    return None, None


def find_last_winner_board(numbers: list, boards: list) -> tuple[list, list]:
    # find and return last_winner_numbers and last_winner_board
    last_winner_numbers = None
    last_winner_board = None
    remaining_board_indices = list(range(len(boards)))

    for i in range(5, len(numbers)):
        temp_numbers = numbers[:i]

        for i in remaining_board_indices:
            if(numbers_on_board(temp_numbers, boards[i])):
                # safe board and numbers
                last_winner_numbers = temp_numbers
                last_winner_board = boards[i]

                # remove board from boards
                remaining_board_indices.remove(i)
    
    return last_winner_numbers, last_winner_board


def calculate_winner_score(winner_numbers, winner_board) -> int:
    """
    1. find the sum of all unmarked numbers on that board; 
    2. multiply that sum by the number that was just called when the board won
    """
    winner_number = int(winner_numbers[-1])
    
    # find unmarked numbers on the board
    unmarked_numbers_sum = 0
    for row in winner_board:
        for i in row:
            if i not in winner_numbers:
                unmarked_numbers_sum += int(i)

    return winner_number * unmarked_numbers_sum


def part_1(numbers: list, boards: list) -> int:
    # find board that wins first
    winner_numbers, winner_board = find_winner_board(numbers, boards)
    return calculate_winner_score(winner_numbers, winner_board)


def part_2(numbers: list, boards: list) -> int:
    # find board which will win last
    last_winner_numbers, last_winner_board = find_last_winner_board(numbers, boards)
    return calculate_winner_score(last_winner_numbers, last_winner_board)


if __name__ == '__main__':
    print(INPUT_FILE)

    example_numbers, example_data = get_input(EXAMPLE_INPUT_FILE)
    example_boards = parse_boards(example_data)
    print(example_numbers)
    print(example_data)

    numbers, data = get_input(INPUT_FILE)
    boards = parse_boards(data)

    # Part 1
    print(part_1(example_numbers, example_boards))
    print(part_1(numbers, boards))

    # Part 2
    print(part_2(example_numbers, example_boards))
    print(part_2(numbers, boards))
