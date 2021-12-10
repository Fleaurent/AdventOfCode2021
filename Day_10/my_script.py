from pathlib import Path
from functools import reduce
from operator import mul

import sys
from typing import no_type_check_decorator

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_10" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_10" / "example_input.txt"


match_closing_brackets = {
    ">": "<",
    ")": "(",
    "}": "{",
    "]": "["
}

match_open_brackets = {
    "<": ">",
    "(": ")",
    "{": "}",
    "[": "]"
}


def get_input(filepath: Path) -> list[str]:
    commands = []
    with open(filepath, "r") as f:
        for command_line in f.readlines():
            commands.append(command_line.strip())

    return commands


def find_corrupted_bracket(command: str) -> str:
    command_queue = []
    for character in command:
        if character in ['<', '(', "[", "{"]:
            command_queue.append(character)
        elif character in ['>', ')', "]", "}"]:
            command_character = command_queue.pop()
            if command_character != match_closing_brackets[character]:
                return character

    return None


def part_1(commands: list[str]) -> int:
    # Some lines are incomplete, but others are corrupted. Find and discard the corrupted lines first.
    # use queue: add <([{ pop }])> -> compare match
    # calculate the syntax error score for a line, take the first illegal character on the line and look it up in the following table:
    error_score = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }
    total_error_score = 0

    command_queue = []
    for command in commands:
        bracket = find_corrupted_bracket(command)

        if bracket is not None:
            total_error_score += error_score[bracket]

    return total_error_score


def find_incomplete_line(command: str) -> str:


    command_queue = []
    for character in command:
        if character in ['<', '(', "[", "{"]:
            command_queue.append(character)
        elif character in ['>', ')', "]", "}"]:
            command_character = command_queue.pop()
            if command_character != match_closing_brackets[character]:
                return None  # corrupted line
    
    # line not corruptes!
    if not command_queue:
        return None # line is complete

    # found incomplete line
    completion_string = ""
    while command_queue:
        completion_string += match_open_brackets[command_queue.pop()]

    return completion_string


def completion_score(completion_string: str) -> int:
    bracket_scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }
    total_score = 0
    for bracket in completion_string:
        total_score = total_score*5 + bracket_scores[bracket]

    return total_score


def part_2(commands: list[str]) -> int:
    scores = []
    for command in commands:
        completion_string = find_incomplete_line(command)
        if completion_string is not None:
            scores.append(completion_score(completion_string))

    return sorted(scores)[len(scores)//2]


if __name__ == '__main__':
    # horizontal position of each crab
    # -> make all of their horizontal positions match while requiring them to spend as little fuel as possible
    print(INPUT_FILE)

    # parse input 
    example_commands = get_input(EXAMPLE_INPUT_FILE)
    print(example_commands)

    commands = get_input(INPUT_FILE)
    print(len(commands))
    print(len(commands[0]))

    # Part 1
    print(part_1(example_commands))
    print(part_1(commands))

    # Part 2
    print(part_2(example_commands))
    print(part_2(commands))
    