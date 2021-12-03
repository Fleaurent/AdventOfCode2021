from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE         = PROJECT_DIR / "Day_3" / "input.txt"
EXAMPLE_INPUT_FILE = PROJECT_DIR / "Day_3" / "example_input.txt"


def get_input(filepath: Path) -> list:
    data = []

    with open(filepath, "r") as f:

        for line in f.readlines():
            data.append(line.strip())

    return data


def part_1(data: list) -> int:
    # optional: parse all bits, then simply sum them up

    gamma_rate = "".join(most_common_bit(data))
    epsilon_rate = "".join(least_common_bit(data))

    # gamma_rate * epsilon_rate
    return int(gamma_rate, 2) * int(epsilon_rate, 2)


def most_common_bit(data: list) -> list:
    # find the most common bit for each bit position over all numbers!
    n_entries = len(data)
    parsed_data = count_ones(data)
    
    return ["1" if i >= (n_entries/2) else "0" for i in parsed_data]


def least_common_bit(data: list) -> list:
    # find the least common bit for each bit position over all numbers!
    n_entries = len(data)
    parsed_data = count_ones(data)

    return ["1" if i < (n_entries/2) else "0" for i in parsed_data]


def count_ones(data: list) -> list:
    # count 1s for each bit position over all numbers!
    n_bits = len(data[0])
    parsed_data = [0] * n_bits

    for line in data:
        for i, bit in enumerate(line):
            if bit == '1':
                parsed_data[i] += 1
    
    return parsed_data


def part_2(data: list) -> int:

    oxygen_generator_rating = get_oxygen_generator_rating(data)
    CO2_scrubber_rating = get_CO2_scrubber_rating(data)

    return oxygen_generator_rating * CO2_scrubber_rating


def get_oxygen_generator_rating(data: list) -> int:
    # filter: remove indice from valid_number set if not valid
    valid_number = {i for i in range(len(data))}
    remove_numbers = set()
    n_bits = len(data[0])

    for bit_i in range(n_bits):
        # 1. calculate gamma rate for remaining valid data
        valid_data = [data[i] for i in valid_number]
        gamma_rate = most_common_bit(valid_data)

        # 2. filter on gamma rate
        for n in valid_number:
            if data[n][bit_i] != gamma_rate[bit_i]:
                remove_numbers.add(n)
        valid_number = valid_number - remove_numbers

        # 3. valid number found yet?
        if(len(valid_number) == 1):
            valid_number = valid_number.pop()
            break

    return int(data[valid_number], 2)


def get_CO2_scrubber_rating(data: list) -> int:
    # filter: remove indice from valid_number set if not valid
    valid_number = {i for i in range(len(data))}
    valid_data = data.copy()
    remove_numbers = set()
    n_bits = len(data[0])

    for bit_i in range(n_bits):
        # 1. calculate gamma rate for remaining valid data
        epsilon_rate = least_common_bit(valid_data)

        # 2. filter on epsilon_rate
        for n in valid_number:
            if data[n][bit_i] != epsilon_rate[bit_i]:
                remove_numbers.add(n)

        valid_number = valid_number - remove_numbers

        # 3. valid number found yet?
        if(len(valid_number) == 1):
            # a) correct indice found!
            valid_number = valid_number.pop()
            break
        else:
            # b) filter
            valid_data = [data[i] for i in valid_number]

    return int(data[valid_number], 2)


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
