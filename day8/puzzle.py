import sys
from pathlib import Path
from pprint import pprint
from collections import defaultdict
import itertools


def do_the_thing(input):
    return part_two(input)


def part_two(input):
    antennas = map_antennas(input.split())

    max_y = len(input.split()) - 1
    max_x = len(input.split()[0]) - 1

    antinodes = find_all_antinodes(antennas, max_y, max_x)

    return len(antinodes)


def find_all_antinodes(antennas, max_y, max_x):
    unique_antinodes = set()

    for same_frequency_antennas in antennas.values():
        for pair in itertools.combinations(same_frequency_antennas, 2):
            antenna1y, antenna1x = pair[0]
            antenna2y, antenna2x = pair[1]

            # add the antennas to the set
            unique_antinodes.add((antenna1y, antenna1x))
            unique_antinodes.add((antenna2y, antenna2x))

            # get diff between two positions
            diff_y = antenna1y - antenna2y
            diff_x = antenna1x - antenna2x

            step_x, step_y = diff_x, diff_y

            while True:
                antinode1 = (antenna1y + step_y, antenna1x + step_x)
                antinode2 = (antenna2y - step_y, antenna2x - step_x)

                if not position_out_of_bounds(max_y, max_x, antinode1):
                    unique_antinodes.add(antinode1)
                    print(f"Added antinode1: {antinode1}")
                if not position_out_of_bounds(max_y, max_x, antinode2):
                    unique_antinodes.add(antinode2)
                    print(f"Added antinode2: {antinode2}")

                # Break the loop if both antinodes are out of bounds
                if position_out_of_bounds(
                    max_y, max_x, antinode1
                ) and position_out_of_bounds(max_y, max_x, antinode2):
                    break

                step_x += diff_x
                step_y += diff_y

    return unique_antinodes


def part_one(input):
    antennas = map_antennas(input.split())
    max_y = len(input.split()) - 1
    max_x = len(input.split()[0]) - 1
    antinodes = find_two_antinodes(antennas, max_y, max_x)

    return len(antinodes)


def find_two_antinodes(antennas, max_y, max_x):
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
