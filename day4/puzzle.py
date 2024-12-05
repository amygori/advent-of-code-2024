import sys
from pathlib import Path
import pprint
import re

pp = pprint.PrettyPrinter(indent=4)


def do_the_thing(input):
    global ROW_COUNT
    global COL_COUNT
    ROW_COUNT = len(input)
    COL_COUNT = len(input[0])

    word_count = search(input)
    return word_count


def search(graph):
    word_count = 0
    for row, line in enumerate(graph):
        for column, letter in enumerate(line):
            # if letter is 'X' then check neighbors
            if letter == "X":
                adjacent_letters = check_adjacent(graph, row, column)
                print(adjacent_letters)
                word_count += len(re.findall(r"XMAS", adjacent_letters))
    return word_count


def check_adjacent(graph, row, column):
    adjacent_letters = ""
    # check four letters in all directions
    for direction in [
        "up",
        "down",
        "left",
        "right",
        "up_left",
        "up_right",
        "down_left",
        "down_right",
    ]:
        adjacent_letters += check_direction(graph, row, column, direction)

    return adjacent_letters


def check_direction(graph, row, column, direction):
    sequential_letters = ""
    for i in range(4):
        if direction == "up":
            if row - i < 0:
                break
            sequential_letters += graph[row - i][column]
        elif direction == "down":
            if row + i >= ROW_COUNT:
                break
            sequential_letters += graph[row + i][column]
        elif direction == "left":
            if column - i < 0:
                break
            sequential_letters += graph[row][column - i]
        elif direction == "right":
            if column + i >= COL_COUNT:
                break
            sequential_letters += graph[row][column + i]
        elif direction == "up_left":
            if row - i < 0 or column - i < 0:
                break
            sequential_letters += graph[row - i][column - i]
        elif direction == "up_right":
            if row - i < 0 or column + i >= COL_COUNT:
                return ""
            sequential_letters += graph[row - i][column + i]
        elif direction == "down_left":
            if row + i >= ROW_COUNT or column - i < 0:
                return ""
            sequential_letters += graph[row + i][column - i]
        elif direction == "down_right":
            if row + i >= ROW_COUNT or column + i >= COL_COUNT:
                return ""
            sequential_letters += graph[row + i][column + i]
    return sequential_letters


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
