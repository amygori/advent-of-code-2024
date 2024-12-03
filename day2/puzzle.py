import sys
from pathlib import Path
from pprint import pprint


def do_the_thing(input):
    input = [[int(item) for item in line.split(" ")] for line in input]
    safe_count = part_one(input)
    return safe_count


def part_one(reports):
    safe_count = 0
    for report in reports:
        monotonic = False
        diff_in_range = False
        pairs = list(zip(report, report[1:]))
        if all(abs(a - b) in range(1, 4) for a, b in pairs):
            diff_in_range = True
        if all(a < b for a, b in pairs):  # increasing
            monotonic = True
        if all(a > b for a, b in pairs):  # decreasing
            monotonic = True
        if diff_in_range and monotonic:
            safe_count += 1
    return safe_count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise TypeError("Please provide a file")
    file_lookup = {"puzzle": "input.txt", "test": "test_input.txt"}
    file_name = file_lookup.get(sys.argv[1])
    if file_name is None:
        raise TypeError("Please provide a valid option, either 'puzzle' or 'test'")
    file = Path(file_name)
    if Path.is_file(Path(file)):
        input = Path.read_text(file).splitlines()
        print(do_the_thing(input))
    else:
        raise TypeError("This is not a file")
