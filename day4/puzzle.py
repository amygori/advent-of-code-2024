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

    count = part_two(input)
    return count


def part_two(input):
    return search_x_mas(input)


def search_x_mas(graph):
    word_count = 0
    for row, line in enumerate(graph):
        for column, letter in enumerate(line):
            # if letter is 'A' then check neighbors
            if letter == "A":
                x1, x2 = check_diagonally_adjacent(graph, row, column, length=2)

                valid_x1 = re.match(r"MAS|SAM", x1) if x1 else None
                valid_x2 = re.match(r"MAS|SAM", x2) if x2 else None
                if valid_x1 is not None and valid_x2 is not None:
                    word_count += 1

    return word_count


def check_diagonally_adjacent(graph, row, column, length=4):
    adjacent_letters = {}

    for direction in [
        "up_left",
        "up_right",
        "down_left",
        "down_right",
    ]:
        adjacent_letters[direction] = check_direction(
            graph, row, column, direction, length=length
        )

    #  x1 is diagonally up left and down right
    try:
        x1 = graph[row - 1][column + 1] + "A" + graph[row + 1][column - 1]
    except IndexError:
        x1 = None

    # x2 is diagonally up right and down left
    try:
        x2 = graph[row - 1][column - 1] + "A" + graph[row + 1][column + 1]
    except IndexError:
        x2 = None

    return (x1, x2)


def part_one(input):
    return search_xmas(input)


def search_xmas(graph):
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
        adjacent_letters += check_direction(graph, row, column, direction, length=3)

    return adjacent_letters


def check_direction(graph, row, column, direction, length):
    sequential_letters = ""
    for i in range(length):
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
