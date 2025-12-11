from util.file_util import read_input_file
from util.run_util import RunTimer

FFT = 0
DAC = 1


class PathCondition:
    visited: dict[tuple[bool, bool], int]
    num_paths: int

    def __init__(self):
        self.visited = {
            (False, False): 0,
            (False, True): 0,
            (True, False): 0,
            (True, True): 0
        }
        self.num_paths = 0


class PathConditions:
    paths: list[PathCondition]
    active: bool

    def __init__(self, active: bool):
        self.active = active
        self.paths = []
        self.paths.append(PathCondition())


class Device:
    name: str
    visits: int
    path_conditions: PathConditions | None
    targets: set[str]
    sources: set[str]
    is_connected_to_start: bool

    def __init__(self, line: str):
        parts = line.split(" ")
        self.name = parts[0][:-1]
        self.visits = 0
        self.path_conditions = None
        self.sources = set()
        self.is_connected_to_start = False
        if len(parts) > 1:
            self.targets = set(parts[1:])
        else:
            self.targets = set()

    def add_path_condition(self, other: PathConditions):

    def __str__(self):
        return f"{self.name} ({self.visits}): {', '.join(self.targets)}"


def parse_input_file(start: str, file_id: int) -> dict[str, Device]:
    lines = read_input_file(11, file_id)
    devices = {"out": Device("out:")}
    for line in lines:
        device = Device(line)
        devices[device.name] = device

    connecting_devices: set[str] = {start}
    while len(connecting_devices) > 0:
        device = devices[connecting_devices.pop()]
        for target_id in device.targets:
            target = devices[target_id]
            if not target.is_connected_to_start:
                connecting_devices.add(target_id)
            target.is_connected_to_start = True
    devices[start].is_connected_to_start = True

    for device in devices.values():
        if device.is_connected_to_start:
            for target in device.targets:
                devices[target].sources.add(device.name)

    return devices


def level11(start: str, path_conditions: bool = False, input_file: int = 0) -> int:
    devices = parse_input_file(start, input_file)
    waiting_devices = set(devices.keys())
    ready_devices: set[str] = {start}
    waiting_devices.remove(start)
    devices[start].path_conditions = PathConditions(path_conditions)
    while len(ready_devices) > 0:
        device = devices[ready_devices.pop()]
        for target_id in device.targets:
            target = devices[target_id]
            target.visits += 1
            target.add_path_condition(device.path_conditions)
            if target.visits == len(target.sources):
                waiting_devices.remove(target.name)
                ready_devices.add(target.name)
    return devices["out"].path_conditions


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Paths (you): {level11("you")}")
    print(f"Paths (svr): {level11("svr", True)}")
    timer.print()


def test_level11():
    assert level11("you") == 5
    assert level11("svr", True, 1) == 2
