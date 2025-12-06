import sys
from typing import List


def read_input_file(level_id: int, file_id: int = 0, strip: bool = True) -> List[str]:
    if "pytest" in sys.modules:
        folder = "test"
        folder_prefix = ""
    else:
        folder = "prod"
        folder_prefix = "../"

    if file_id == 0:
        file = ""
    else:
        file = f"-{file_id}"

    input_file = open(f"{folder_prefix}input-files/{folder}/level{'{:02d}'.format(level_id)}{file}.txt", "r")
    lines = input_file.readlines()
    if strip:
        lines = [line.strip() for line in lines]
    return lines
