import sys
from pathlib import Path
from pprint import pprint


def do_the_thing(input):
    right_locations = []
    left_locations = []
    for index, pair in enumerate(input):
        right, left = pair.split()
        right_locations.append(right)
        left_locations.append(left)
    total_distance = 0
    right_locations = sorted(right_locations)
    left_locations = sorted(left_locations)
    for idx, num in enumerate(right_locations):
        right = int(num)
        left = int(left_locations[idx])
        total_distance += abs(int(num) - int(left_locations[idx]))
    return total_distance


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
