from util.file_util import read_input_file
from util.run_util import RunTimer


def parse_input_file() -> list[int]:
    lines = read_input_file(1)
    directions = [int(line[1:]) * (-1 if line[0] == "L" else 1) for line in lines]
    return directions


def level1() -> tuple[int, int]:
    directions = parse_input_file()
    dial = 50
    times_ended_on_0 = 0
    times_passed_0 = 0
    for direction in directions:
        if direction == 0:
            continue

        started_on_zero = dial == 0
        times_passed, dial = divmod(dial + direction, 100)
        times_passed = abs(times_passed)
        if direction < 0:
            if dial == 0:
                times_passed += 1
            if started_on_zero:
                times_passed -= 1
        times_passed_0 += times_passed
        if dial == 0:
            times_ended_on_0 += 1
    return times_ended_on_0, times_passed_0


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Safe code: {level1()}")
    timer.print()


def test_level1():
    assert level1() == (3, 6)
