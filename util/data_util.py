from typing import TypeVar


def transpose(a_list: list):
    # https://www.geeksforgeeks.org/python-transpose-elements-of-two-dimensional-list/
    return list(map(lambda x: list(x), zip(*a_list)))


def create_2d_list(length: int, height: int, value) -> list[list]:
    if callable(value):
        return [[value() for _ in range(length)] for _ in range(height)]
    else:
        return [[value for _ in range(length)] for _ in range(height)]


T = TypeVar("T")


def convert_string(line: str, a_type) -> list[T]:
    return list(map(a_type, line))


def convert_string_list(lines: list[str], enum_type) -> list[list[T]]:
    return list(map(lambda line: convert_string(line, enum_type), lines))


def split_input_when_empty(lines: list[str]) -> list[list[str]]:
    split_list = []
    last_split = 0
    try:
        split = lines.index("")
        while split != -1:
            split_list.append(lines[last_split:split])
            last_split = split + 1
            split = lines.index("", split + 1)
    except ValueError:
        split_list.append(lines[last_split:])
        return split_list
