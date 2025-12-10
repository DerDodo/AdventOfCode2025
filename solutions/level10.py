from util.file_util import read_input_file
from util.run_util import RunTimer


class Button:
    signals: set[int]

    def __init__(self, line: str):
        self.signals = set(map(int, line[1:-1].split(",")))

    def press_during_startup(self, lights: list[bool]) -> list[bool]:
        new_lights = lights.copy()
        for signal in self.signals:
            new_lights[signal] = not new_lights[signal]
        return new_lights

    def __str__(self) -> str:
        return f"[{', '.join(map(str, self.signals))}]"


class Machine:
    id_counter = 0
    id: int
    target_lights: list[bool]
    buttons: list[Button]
    joltage_target: list[int]
    button_lookup: dict[int, list[int]]
    hash_multiplier: int
    lookup_cache: dict[int, list[int]]

    def __init__(self, line: str):
        self.id = Machine.id_counter
        Machine.id_counter += 1

        parts = line.split(" ")
        self.target_lights = [True if light == "#" else False for light in parts[0][1:-1]]
        self.buttons = list(map(Button, parts[1:-1]))
        self.buttons.sort(key=lambda b: len(b.signals), reverse=True)
        self.joltage_target = list(map(int, parts[-1][1:-1].split(",")))
        self.hash_multiplier = 100 #max(self.joltage_target) + 1
        self.lookup_cache = dict()

    def is_done(self, lights: list[bool]) -> bool:
        for i in range(len(lights)):
            if self.target_lights[i] != lights[i]:
                return False
        if len(lights) != len(self.target_lights):
            raise RuntimeError("This should not happen!")
        return True


def calc_next_options(machine: Machine, last_button: int, lights: list[bool]) -> list[tuple[int, list[bool]]]:
    new_options = []
    for i in range(len(machine.buttons)):
        if i != last_button:
            new_options.append((i, machine.buttons[i].press_during_startup(lights)))
    return new_options


def calc_min_presses_to_turn_on(machine: Machine) -> int:
    initial_lights = [False] * len(machine.target_lights)

    if machine.is_done(initial_lights):
        return 0

    all_options: list[tuple[int, list[bool]]] = []
    for i in range(len(machine.buttons)):
        lights = machine.buttons[i].press_during_startup(initial_lights)
        if machine.is_done(lights):
            return 1
        all_options.append((i, lights))
    for num_button_presses in range(1, 1000):
        new_all_options = []
        for option in all_options:
            new_options = calc_next_options(machine, option[0], option[1])
            for new_option in new_options:
                if machine.is_done(new_option[1]):
                    return num_button_presses + 1
            new_all_options.extend(new_options)
        all_options = new_all_options
    raise RuntimeError("Could not find solution!")


def calc_joltages_to_influence(joltage_left: list[int], max_joltage: int) -> list[int]:
    buttons = []
    for i in range(len(joltage_left)):
        if joltage_left[i] == max_joltage:
            buttons.append(i)
    return buttons


def calc_buttons_to_press(machine: Machine, joltage_left: list[int], max_joltage: int) -> list[int]:
    joltages_to_influence = calc_joltages_to_influence(joltage_left, max_joltage)
    cache_id = sum([2 ** d for d in joltages_to_influence])
    if cache_id in machine.lookup_cache:
        target_buttons = machine.lookup_cache[cache_id]
    else:
        target_buttons = []
        target_buttons_2 = []
        for button_i in range(len(machine.buttons)):
            button = machine.buttons[button_i]
            count_joltages = 0
            for joltage in joltages_to_influence:
                if joltage in button.signals:
                    count_joltages += 1

            if count_joltages == len(joltages_to_influence):
                target_buttons.append(button_i)
            elif count_joltages > 0:
                target_buttons_2.append(button_i)
        target_buttons.extend(target_buttons_2)
        machine.lookup_cache[cache_id] = target_buttons

    filtered_target_buttons = []
    for button_i in target_buttons:
        press_button = True
        for joltage in machine.buttons[button_i].signals:
            if joltage_left[joltage] == 0:
                press_button = False
                break
        if press_button:
            filtered_target_buttons.append(button_i)

    if len(filtered_target_buttons) == 0:
        return filtered_target_buttons

    buttons_to_press = []
    limit = 0
    upper_limit = max(max_joltage, 15)
    while len(buttons_to_press) == 0 and limit <= upper_limit:
        limit += 5
        for button_i in filtered_target_buttons:
            press_button = True
            for joltage in machine.buttons[button_i].signals:
                if max_joltage - joltage_left[joltage] > limit:
                    press_button = False
                    break
            if press_button:
                buttons_to_press.append(button_i)
    return buttons_to_press


def calc_min_presses_to_configure_joltage_dfs(machine: Machine, press_hash: int, min_found: int, num_button_presses: int, joltage_left: list[int]) -> int:
    if num_button_presses == min_found:
        return min_found

    max_joltage = max(joltage_left)
    if num_button_presses + max_joltage >= min_found:
        return min_found

    buttons_to_press = calc_buttons_to_press(machine, joltage_left, max_joltage)
    for button_i in buttons_to_press:
        new_press_hash = press_hash + machine.hash_multiplier ** button_i
        if new_press_hash in calc_min_presses_to_configure_joltage_dfs.seen:
            continue
        calc_min_presses_to_configure_joltage_dfs.seen.add(new_press_hash)

        button = machine.buttons[button_i]

        new_joltages = []
        num_0 = 0

        for i in range(len(joltage_left)):
            if i in button.signals:
                value = joltage_left[i] - 1
            else:
                value = joltage_left[i]
            new_joltages.append(value)
            if value == 0:
                num_0 += 1

        if num_0 == len(new_joltages):
            return num_button_presses + 1

        min_found = calc_min_presses_to_configure_joltage_dfs(machine, new_press_hash, min_found, num_button_presses + 1, new_joltages)

    return min_found


calc_min_presses_to_configure_joltage_dfs.seen = set()


def calc_min_presses_to_configure_joltage(machine: Machine) -> int:
    timer = RunTimer()
    min_presses = calc_min_presses_to_configure_joltage_dfs(machine, 0, 1000000, 0, machine.joltage_target.copy())
    print(f"Machine {calc_min_presses_to_configure_joltage.i}: {min_presses} - {timer.get_time()} seconds")
    calc_min_presses_to_configure_joltage.i += 1
    return min_presses


calc_min_presses_to_configure_joltage.i = 0


def parse_input_file() -> list[Machine]:
    lines = read_input_file(10)
    return list(map(Machine, lines))


def level10() -> tuple[int, int]:
    machines = parse_input_file()

    sum_to_turn_on = sum(map(calc_min_presses_to_turn_on, machines))
    print("Startup complete. Starting configuration...")
    sum_to_configure_joltage = sum(map(calc_min_presses_to_configure_joltage, machines))
    
    return sum_to_turn_on, sum_to_configure_joltage


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Button presses: {level10()}")
    timer.print()


def test_level10():
    assert level10() == (7, 33)
