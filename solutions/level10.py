from enum import Enum

from util.file_util import read_input_file
from util.math_util import Position
from util.run_util import RunTimer


class Machine:
    lights: list[bool]
    buttons: list[list[int]]
    joltage: list[int]

    def __init__(self, line: str):
        parts = line.split(" ")
        self.lights = [True if light == "#" else False for light in parts[0][1:-1]]
        self.buttons = [list(map(int, button[1:-1].split(","))) for button in parts[1:-1]]
        self.joltage = list(map(int, parts[-1][1:-1].split(",")))


def parse_input_file() -> list[Machine]:
    lines = read_input_file(10)
    return list(map(Machine, lines))


def level10() -> tuple[int, int]:
    machines = parse_input_file()

    sum_min_button_presses
    
    return 0, 0


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Button presses: {level10()}")
    timer.print()


def test_level10():
    assert level10() == (7, 0)
