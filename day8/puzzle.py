import sys
from pathlib import Path
from pprint import pprint
from collections import defaultdict
import itertools


def do_the_thing(input):
    antennas = map_antennas(input.split())
    max_y = len(input.split()) - 1
    max_x = len(input.split()[0]) - 1
    antinodes = find_antinodes(antennas, max_y, max_x)

    return len(antinodes)


def find_antinodes(antennas, max_y, max_x):
    unique_antinodes = set()
    for same_frequency_antennas in antennas.values():
        for pair in itertools.combinations(same_frequency_antennas, 2):
            antenna1y, antenna1x = pair[0]
            antenna2y, antenna2x = pair[1]

            # get diff between two positions
            diff_y = antenna1y - antenna2y
            diff_x = antenna1x - antenna2x

            # get two antinodes on either side by adding and subtracting diff
            antinode1 = (antenna1y + diff_y, antenna1x + diff_x)
            antinode2 = (antenna2y - diff_y, antenna2x - diff_x)

            # check if antinode is out of bounds
            for antinode in [antinode1, antinode2]:
                if not position_out_of_bounds(max_y, max_x, antinode):
                    unique_antinodes.add(antinode)

    return unique_antinodes


def map_antennas(input):
    antennas = defaultdict(list)
    for y in range(len(input)):
        for x in range(len(input[0])):
            if input[y][x].isalnum():
                antennas[input[y][x]].append((y, x))
    return antennas


def position_out_of_bounds(max_y, max_x, position):
    y, x = position
    return y < 0 or x > max_x or y > max_y or x < 0


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
        pprint(do_the_thing(input))
    else:
        raise TypeError("This is not a file")
