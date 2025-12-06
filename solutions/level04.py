from enum import Enum

from util.data_util import convert_string_list
from util.file_util import read_input_file
from util.math_util import Area, NEWSDirections, Direction, Position
from util.run_util import RunTimer


class Field(Enum):
    Free = "."
    PaperRoll = "@"


class Room(Area):
    remaining_rolls: set[Position]

    def __init__(self, lines: list[str]):
        super().__init__(convert_string_list(lines, Field))
        self.remaining_rolls = set()
        for field in self:
            if self[field] == Field.PaperRoll:
                self.remaining_rolls.add(field)

    def calc_movable_rolls(self) -> set[Position]:
        movable_rolls = set()
        for field in self.remaining_rolls:
            if self[field] == Field.PaperRoll:
                num_adjacent_rolls = sum([1 if self.fast_safe_check(field.x + direction.x, field.y + direction.y, Field.PaperRoll) else 0 for direction in Direction])
                if num_adjacent_rolls < 4:
                    movable_rolls.add(field)
        return movable_rolls

    def remove_rolls(self) -> int:
        movable_rolls = self.calc_movable_rolls()
        if len(movable_rolls) == 0:
            return 0

        self.remaining_rolls = self.remaining_rolls - movable_rolls
        for roll in movable_rolls:
            self[roll] = Field.Free

        return len(movable_rolls)


def parse_input_file() -> Room:
    return Room(read_input_file(4))


def level4() -> tuple[int, int]:
    room = parse_input_file()
    removed_rolls = num_movable_rolls_at_the_start = num_movable_rolls = room.remove_rolls()

    while removed_rolls != 0:
        removed_rolls = room.remove_rolls()
        num_movable_rolls += removed_rolls

    return num_movable_rolls_at_the_start, num_movable_rolls


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Accessible paper rolls: {level4()}")
    timer.print()


def test_level4():
    assert level4() == (13, 43)
