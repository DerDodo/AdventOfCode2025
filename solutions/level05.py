from util.file_util import read_input_file
from util.run_util import RunTimer


def merge_ranges(fresh_ingredients: list[tuple[int, int]]) -> list[tuple[int, int]]:
    mem_num_ranges = 0
    while mem_num_ranges != len(fresh_ingredients):
        mem_num_ranges = len(fresh_ingredients)
        fresh_ingredients.sort()
        new_fresh_ingredients = []
        i = 0
        while i < len(fresh_ingredients) - 1:
            left = fresh_ingredients[i]
            right = fresh_ingredients[i + 1]
            if right[0] <= left[1]:
                new_fresh_ingredients.append((left[0], max(left[1], right[1])))
                i += 2
            else:
                new_fresh_ingredients.append((left[0], left[1]))
                i += 1
        if i == len(fresh_ingredients) - 1:
            new_fresh_ingredients.append(fresh_ingredients[-1])
        new_fresh_ingredients.sort()
        fresh_ingredients = new_fresh_ingredients

    return fresh_ingredients


def parse_input_file() -> tuple[list[tuple[int, int]], set[int]]:
    lines = read_input_file(5)
    line_i = 0

    fresh_ingredients = []
    while lines[line_i] != "":
        parts = lines[line_i].split("-")
        fresh_ingredients.append((int(parts[0]), int(parts[1])))
        line_i += 1

    fresh_ingredients = merge_ranges(fresh_ingredients)

    line_i += 1

    ingredients = set()
    while line_i < len(lines):
        ingredients.add(int(lines[line_i]))
        line_i += 1

    return fresh_ingredients, ingredients


def level5() -> tuple[int, int]:
    fresh_ingredients, ingredients = parse_input_file()

    num_fresh_ingredients = 0
    for ingredient in ingredients:
        for fresh_ingredient_range in fresh_ingredients:
            if fresh_ingredient_range[0] <= ingredient <= fresh_ingredient_range[1]:
                num_fresh_ingredients += 1
                break

    num_available_fresh_ingredients = sum([ing[1] + 1 - ing[0] for ing in fresh_ingredients])
    return num_fresh_ingredients, num_available_fresh_ingredients


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Fresh ingredients: {level5()}")
    timer.print()


def test_level5():
    assert level5() == (3, 14)
