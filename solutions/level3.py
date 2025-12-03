from util.file_util import read_input_file
from util.run_util import RunTimer


def parse_input_file() -> list[list[int]]:
    lines = read_input_file(3)
    return [[int(battery) for battery in line] for line in lines]


def calc_joltage(bank: list[int], indices: list[int]) -> int:
    joltage = 0
    for index in indices:
        joltage = joltage * 10 + bank[index]
    return joltage


def calc_max_joltage(bank: list[int], num_batteries: int) -> int:
    indices = list(range(len(bank) - num_batteries, len(bank)))
    for index_to_move in range(num_batteries):
        index_to_stop = -1 if index_to_move == 0 else indices[index_to_move - 1]
        for index_to_check in range(indices[index_to_move] - 1, index_to_stop, -1):
            if bank[index_to_check] >= bank[indices[index_to_move]]:
                indices[index_to_move] = index_to_check
    return calc_joltage(bank, indices)


def level3(num_batteries: int) -> int:
    banks = parse_input_file()
    return sum([calc_max_joltage(bank, num_batteries) for bank in banks])


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Joltage: {level3(2), level3(12)}")
    timer.print()


def test_level3():
    assert level3(2) == 357
    assert level3(12) == 3121910778619
