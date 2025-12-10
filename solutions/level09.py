from enum import Enum

from util.file_util import read_input_file
from util.math_util import Position
from util.run_util import RunTimer


class Tile(Enum):
    Free = "."
    Red = "#"
    Green = "X"


def create_position(line: str) -> Position:
    parts = line.split(",")
    return Position(int(parts[0]), int(parts[1]))


def parse_input_file() -> list[Position]:
    lines = read_input_file(9)
    return list(map(create_position, lines))


def level9() -> tuple[int, int]:
    tiles = parse_input_file()
    max_area = max_x = max_y = 0
    min_x = min_y = 1000000000
    for i in range(len(tiles)):
        min_x = min(min_x, tiles[i].x)
        max_x = max(max_x, tiles[i].x)
        min_y = min(min_y, tiles[i].y)
        max_y = max(max_y, tiles[i].y)

        for j in range(i, len(tiles)):
            max_area = max(max_area, abs(tiles[i].x - tiles[j].x + 1) * abs(tiles[i].y - tiles[j].y + 1))

    for i in range(len(tiles)):
        tiles[i] = Position(tiles[i][0] - min_x, tiles[i][1] - min_y)
    
    return max_area, 0


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Area: {level9()}")
    timer.print()


def test_level9():
    assert level9() == (50, 24)
