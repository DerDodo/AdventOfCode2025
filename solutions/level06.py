import re
from enum import Enum
from math import prod

from util.file_util import read_input_file
from util.run_util import RunTimer


class Operation(Enum):
    Multiply = "*"
    Add = "+"

    def exec(self, numbers: list[int]) -> int:
        if self == Operation.Multiply:
            return prod(numbers)
        else:
            return sum(numbers)


def parse_input_file1() -> list[tuple[Operation, list[int]]]:
    lines = read_input_file(6)
    number_lines = []
    for i in range(len(lines) - 1):
        line = re.sub('  +', ' ', lines[i])
        number_lines.append(list(map(int, line.split(" "))))
    operation_line = re.sub('  +', ' ', lines[-1])
    operations = [Operation(char) for char in operation_line.split(" ")]

    challenges = []
    for column in range(len(operations)):
        numbers = []
        for row in range(len(number_lines)):
            numbers.append(number_lines[row][column])
        challenges.append((operations[column], numbers))

    return challenges


def parse_input_file2() -> list[tuple[Operation, list[int]]]:
    lines = read_input_file(6, strip=False)
    challenges = []
    numbers = []
    operation = None
    for col in range(len(lines[-1])):
        number = 0
        for row in range(len(lines) - 1):
            if lines[row][col].isnumeric():
                number = number * 10 + int(lines[row][col])

        if lines[-1][col] != " ":
            operation = Operation(lines[-1][col])

        if number == 0:
            challenges.append((operation, numbers))
            numbers = []
        else:
            numbers.append(number)
    challenges.append((operation, numbers))
    return challenges


def solve(challenges: list[tuple[Operation, list[int]]]) -> int:
    return sum([challenge[0].exec(challenge[1]) for challenge in challenges])


def level6() -> tuple[int, int]:
    return solve(parse_input_file1()), solve(parse_input_file2())


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Total sum: {level6()}")
    timer.print()


def test_level6():
    assert level6() == (4277556, 3263827)
