from util.file_util import read_input_file
from util.run_util import RunTimer


class Device:
    name: str
    visits: int
    targets: set[str]
    sources: set[str]
    is_connected_to_start: bool
    paths: dict[bool, dict[bool, int]]
    use_path_conditions: bool

    def __init__(self, line: str, use_path_conditions: bool, start: str):
        parts = line.split(" ")
        self.name = parts[0][:-1]
        self.visits = 0
        self.sources = set()
        self.is_connected_to_start = False

        if len(parts) > 1:
            self.targets = set(parts[1:])
        else:
            self.targets = set()

        self.use_path_conditions = use_path_conditions
        self.paths = {
            # [dac][fft]: num_paths
            False: {
                False: 0,
                True: 0
            },
            True: {
                False: 0,
                True: 0
            }
        }

        if self.name == start:
            if use_path_conditions:
                self.paths[False][False] = 1
            else:
                self.paths[True][True] = 1

    def _add_visit_dac(self, other):
        self.paths[True][False] += other.paths[False][False]
        self.paths[True][True] += other.paths[False][True]

    def _add_visit_fft(self, other):
        self.paths[False][True] += other.paths[False][False]
        self.paths[True][True] += other.paths[True][False]

    def add_paths(self, other):
        if not self.use_path_conditions:
            self.paths[True][True] += other.paths[True][True]
        elif self.name == "dac":
            self._add_visit_dac(other)
        elif self.name == "fft":
            self._add_visit_fft(other)
        else:
            self.paths[False][False] += other.paths[False][False]
            self.paths[False][True] += other.paths[False][True]
            self.paths[True][False] += other.paths[True][False]
            self.paths[True][True] += other.paths[True][True]

    def __str__(self):
        return f"{self.name} ({self.visits}): {', '.join(self.targets)}"


def parse_input_file(start: str, path_conditions: bool, file_id: int) -> dict[str, Device]:
    lines = read_input_file(11, file_id)
    devices = {"out": Device("out:", path_conditions, start)}
    for line in lines:
        device = Device(line, path_conditions, start)
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
    devices = parse_input_file(start, path_conditions, input_file)

    waiting_devices = set(devices.keys())
    ready_devices: set[str] = {start}
    waiting_devices.remove(start)

    while len(ready_devices) > 0:
        device = devices[ready_devices.pop()]
        for target_id in device.targets:
            target = devices[target_id]
            target.visits += 1
            target.add_paths(device)
            if target.visits == len(target.sources):
                waiting_devices.remove(target.name)
                ready_devices.add(target.name)

    return devices["out"].paths[True][True]


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Paths (you): {level11('you')}")
    print(f"Paths (svr): {level11('svr', True)}")
    timer.print()


def test_level11():
    assert level11("you") == 5
    assert level11("svr", False, 1) == 8
    assert level11("svr", True, 1) == 2
