from enum import Enum

from util.data_util import convert_string_list
from util.file_util import read_input_file
from util.math_util import Area, Direction, Position
from util.run_util import RunTimer


class Field(Enum):
    Free = "."
    Splitter = "^"
    Tachyon = "S"


def parse_input_file() -> Area:
    lines = read_input_file(7)
    return Area(convert_string_list(lines, Field))


def calc_num_tachyons(tachyons: dict[Position, int], position: Position, num_timelines: int) -> int:
    if position in tachyons:
        return tachyons[position] + num_timelines
    else:
        return num_timelines


def level7() -> tuple[int, int]:
    area = parse_input_file()
    tachyons = {area.find_first(Field.Tachyon): 1}
    num_splits = 0
    for _ in range(area.get_height() - 1):
        new_tachyons = {}
        for tachyon in tachyons.items():
            new_position = tachyon[0] + Direction.South
            if area[new_position] == Field.Free:
                new_tachyons[new_position] = calc_num_tachyons(new_tachyons, new_position, tachyon[1])
            elif area[new_position] == Field.Splitter:
                num_splits += 1
                left = new_position + Direction.West
                right = new_position + Direction.East
                new_tachyons[left] = calc_num_tachyons(new_tachyons, left, tachyon[1])
                new_tachyons[right] = calc_num_tachyons(new_tachyons, right, tachyon[1])
        tachyons = new_tachyons
    return num_splits, sum(tachyons.values())


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Num beams, timelines: {level7()}")
    timer.print()


def test_level7():
    assert level7() == (21, 40)
