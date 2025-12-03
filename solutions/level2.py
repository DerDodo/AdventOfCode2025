from util.file_util import read_input_file
from util.math_util import count_digits
from util.run_util import RunTimer


def to_range(id_range) -> list[int]:
    return [int(part) for part in id_range.split("-")]


def parse_input_file() -> list[list[int]]:
    lines = read_input_file(2)
    ranges = lines[0].split(",")
    return [to_range(id_range) for id_range in ranges]


def prepare_range(num_parts: int, input_id_range: list[int]) -> list[int]:
    id_range = [input_id_range[0], input_id_range[1]]
    len0 = count_digits(id_range[0])
    len1 = count_digits(id_range[1])
    if len0 != len1:
        if len0 % num_parts != 0:
            id_range[0] = int('1' + '0' * len0)
        if len1 % num_parts != 0:
            id_range[1] = int('9' * len0)
    return id_range


def is_pattern_possible(num_parts: int, id_range: list[int]) -> bool:
    len0 = count_digits(id_range[0])
    len1 = count_digits(id_range[1])
    part_length = len1 // num_parts
    return (len0 == len1 and len0 % num_parts == 0) or part_length == 0


def save_calc_invalid_ids(num_parts: int, id_range: list[int]) -> set[int]:
    invalid_ids = set()
    len1 = count_digits(id_range[1])
    part_length = len1 // num_parts
    id_min_l = int(str(id_range[0])[0:part_length])
    id_max_l = int(str(id_range[1])[0:part_length])
    for i in range(id_min_l, id_max_l + 1):
        check_id = int(str(i) * num_parts)
        if id_range[0] <= check_id <= id_range[1]:
            invalid_ids.add(check_id)
    return invalid_ids


def calc_invalid_ids(num_parts: int, input_id_range: list[int]) -> set[int]:
    id_range = prepare_range(num_parts, input_id_range)

    if not is_pattern_possible(num_parts, id_range):
        return set()

    return save_calc_invalid_ids(num_parts, id_range)


def level2() -> tuple[int, int]:
    id_ranges = parse_input_file()
    invalid_ids = set()
    invalid_two_part_ids = set()
    for id_range in id_ranges:
        for i in range(2, count_digits(id_range[1]) + 1):
            new_invalid_ids = calc_invalid_ids(i, id_range)
            invalid_ids.update(new_invalid_ids)
            if i == 2:
                invalid_two_part_ids.update(new_invalid_ids)
    return sum(invalid_two_part_ids), sum(invalid_ids)


if __name__ == '__main__':
    timer = RunTimer()
    print(f"invalid ID sum: {level2()}")
    timer.print()


def test_level2():
    assert level2() == (1227775554, 4174379265)
