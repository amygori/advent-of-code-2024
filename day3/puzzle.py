import sys
from pathlib import Path
import re
from functools import reduce


def do_the_thing(input):
    return part_one(input)


def part_one(input):
    total = 0
    pairs = re.findall(r"(?:mul)\((\d+,\d+)\)", input)
    for factors in [pair.split(",") for pair in pairs]:
        result = reduce(lambda x, y: int(x) * int(y), factors)
        total += result
    return total


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise TypeError("Please provide a file")
    file_lookup = {"puzzle": "input.txt", "test": "test_input.txt"}
    file_name = file_lookup.get(sys.argv[1])
    if file_name is None:
        raise TypeError("Please provide a valid option, either 'puzzle' or 'test'")
    file = Path(file_name)
    if Path.is_file(Path(file)):
        input = Path.read_text(file)
        print(do_the_thing(input))
    else:
        raise TypeError("This is not a file")
