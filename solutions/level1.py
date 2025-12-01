from collections import defaultdict

from util.file_util import read_input_file
from util.run_util import RunTimer


def parse_input_file() -> tuple[list[int], list[int], dict[int, int]]:
    lines = read_input_file(1)
    parts_list = list(map(lambda line: line.split(" "), lines))

    left = list(map(lambda parts: int(parts[0]), parts_list))
    right = list(map(lambda parts: int(parts[-1]), parts_list))

    right_amount = defaultdict(int)
    for item in right:
        right_amount[item] += 1

    left.sort()
    right.sort()

    return left, right, right_amount


def level1() -> tuple[int, int]:
    left, right, right_amount = parse_input_file()
    total_distance = 0
    total_similarity = 0
    for i in range(len(left)):
        total_distance += abs(left[i] - right[i])
        total_similarity += left[i] * right_amount[left[i]]
    return total_distance, total_similarity


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Total distance: {level1()}")
    timer.print()


def test_level1():
    assert level1() == (11, 31)
