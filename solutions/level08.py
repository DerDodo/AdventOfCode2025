import math
from collections import defaultdict

from util.file_util import read_input_file
from util.run_util import RunTimer


class Box:
    x: int
    y: int
    z: int
    circuit: None | int

    def __init__(self, line: str):
        parts = line.split(",")
        self.x, self.y, self.z = map(int, parts)
        self.circuit = None

    def distance(self, other) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def __str__(self) -> str:
        return f"Box({'/' if self.circuit is None else str(self.circuit)}): {self.x}, {self.y}, {self.z}"


def parse_input_file() -> list[Box]:
    lines = read_input_file(8)
    return list(map(Box, lines))


def get_circuit_id_for_connection(box1: Box, box2: Box) -> int:
    if box1.circuit is None and box2.circuit is not None:
        return box2.circuit
    elif box1.circuit is not None and box2.circuit is None:
        return box1.circuit
    else:
        get_circuit_id_for_connection.next_id += 1
        return get_circuit_id_for_connection.next_id - 1


get_circuit_id_for_connection.next_id = 0


def calc_distances(boxes: list[Box]) -> list[tuple[float, Box, Box]]:
    distances: list[tuple[float, Box, Box]] = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            distance = boxes[i].distance(boxes[j])
            distances.append((distance, boxes[i], boxes[j]))
    distances.sort()
    return distances


def level8(part1_connection_limit: int) -> tuple[int, int]:
    boxes = parse_input_file()
    solution_part1 = 0

    distances = calc_distances(boxes)

    circuit_sizes: dict[int, int] = defaultdict(int)
    for i in range(len(distances)):
        box1 = distances[i][1]
        box2 = distances[i][2]
        if box1.circuit is None or box2.circuit is None:
            circuit_id = get_circuit_id_for_connection(box1, box2)

            if box1.circuit is None:
                box1.circuit = circuit_id
                circuit_sizes[circuit_id] = circuit_sizes[circuit_id] + 1

            if box2.circuit is None:
                box2.circuit = circuit_id
                circuit_sizes[circuit_id] = circuit_sizes[circuit_id] + 1

        elif box1.circuit is not None and box1.circuit != box2.circuit:
            circuit_sizes[box1.circuit] = circuit_sizes[box1.circuit] + circuit_sizes[box2.circuit]
            circuit_sizes[box2.circuit] = 0

            old_circuit_id = box2.circuit
            for box in boxes:
                if box.circuit == old_circuit_id:
                    box.circuit = box1.circuit

        if circuit_sizes[box1.circuit] == len(boxes):
            solution_part2 = box1.x * box2.x
            return solution_part1, solution_part2

        if i == part1_connection_limit - 1:
            biggest_circuits = list(circuit_sizes.values())
            biggest_circuits.sort(reverse=True)
            solution_part1 = biggest_circuits[0] * biggest_circuits[1] * biggest_circuits[2]

    raise RuntimeError("Couldn't connect all boxes?")


if __name__ == '__main__':
    timer = RunTimer()
    print(f"Circuits: {level8(1000)}")
    timer.print()


def test_level8():
    assert level8(10) == (40, 25272)
