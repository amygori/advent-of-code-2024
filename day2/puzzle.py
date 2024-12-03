import sys
from pathlib import Path
from pprint import pprint


def do_the_thing(input):
    input = [[int(item) for item in line.split(" ")] for line in input]
    safe_count, possibly_safe_reports = part_one(input)
    safe_count += part_two(possibly_safe_reports)
    return safe_count


def part_two(reports):
    safe_count = 0
    for report in reports:
        for idx, num in enumerate(report):
            report_copy = report[:]
            report_copy.pop(idx)
            if is_safe(report_copy):
                safe_count += 1
                break
            else:
                continue
    return safe_count


def part_one(reports):
    safe_count = 0
    possibly_safe_reports = []
    for report in reports:
        if is_safe(report):
            safe_count += 1
        else:
            possibly_safe_reports.append(report)
    return (safe_count, possibly_safe_reports)


def is_safe(report):
    pairs = list(zip(report, report[1:]))
    monotonic = False
    diff_in_range = False
    if all(abs(a - b) in range(1, 4) for a, b in pairs):
        diff_in_range = True
    if all(a < b for a, b in pairs):  # increasing
        monotonic = True
    if all(a > b for a, b in pairs):  # decreasing
        monotonic = True
    return diff_in_range and monotonic


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
