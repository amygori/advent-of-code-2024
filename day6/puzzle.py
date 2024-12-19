import sys
from pathlib import Path
from collections import defaultdict


def do_the_thing(input):
    # return part_one(input)
    # modify the graph by putting an obstacle in all the visited spaces
    # detect a loop by tracking when a spot has been visited 4 times
    # when the guard turns, start tracking the location and the direction.
    # If we encounter the same location and direction again,
    return part_two(input)


def part_two(input):
    obstruction_count = 0
    guard_starting_position = get_starting_position(input)
    graphs = generate_test_graphs(input, guard_starting_position)
    twice_visited_positions = defaultdict(list)
    graphs_with_loops = []
    for graph in graphs:
        loop_position = detect_loop(graph, guard_starting_position)
        print("Loop position: ", loop_position)
        if loop_position is not None:
            graphs_with_loops.append(graph)
            twice_visited_positions[loop_position[0]].append(loop_position[1])

    return twice_visited_positions


def generate_test_graphs(input, guard_starting_position):
    positions = visited_positions(input)
    obstructed_graphs = []
    for position in positions:
        if position == guard_starting_position:
            continue
        graph = input[:]
        row = graph[position[0]]
        index = position[1]
        new_row = row[:index] + "$" + row[index + 1 :]
        graph[position[0]] = new_row
        # print("Adding obstacle at position ", position)
        obstructed_graphs.append(graph)

    return obstructed_graphs


def detect_loop(input, guard_position):
    guard_direction = "up"
    graph = input
    edge_reached = False
    loop_position = None
    visited_positions = defaultdict(list)

    while not edge_reached:
        next_move = move(guard_position, guard_direction, graph)
        if guard_direction in visited_positions.get(next_move, []):
            loop_position = (next_move, guard_direction)
            break
        if position_is_edge(graph, next_move):
            print("Edge reached")
            edge_reached = True
            break
        elif check_for_obstacle(graph, next_move):
            guard_direction = turn_right(guard_direction)
            continue
        else:
            guard_position = next_move
            visited_positions[guard_position].append(guard_direction)
    return loop_position


def part_one(input):
    return len(set(visited_positions(input)))


def visited_positions(input):
    guard_position = get_starting_position(input)

    guard_direction = "up"
    visited_positions = []
    graph = input
    edge_reached = False
    while edge_reached is False:
        next_move = move(guard_position, guard_direction, graph)

        if position_is_edge(graph, next_move):
            print("Edge reached")
            edge_reached = True
            break
        elif check_for_obstacle(graph, next_move):
            guard_direction = turn_right(guard_direction)
            continue
        else:
            guard_position = next_move
            visited_positions.append(guard_position)
    return visited_positions


def turn_right(guard_direction):
    turn = {
        "up": "right",
        "right": "down",
        "down": "left",
        "left": "up",
    }
    return turn[guard_direction]


def move(guard_position, direction, graph):
    moves = {
        "up": (guard_position[0] - 1, guard_position[1]),
        "down": (guard_position[0] + 1, guard_position[1]),
        "left": (guard_position[0], guard_position[1] - 1),
        "right": (guard_position[0], guard_position[1] + 1),
    }

    if direction not in moves.keys():
        raise ValueError("Invalid direction")
    return moves[direction]


def check_for_obstacle(graph, position):
    return (
        graph[position[0]][position[1]] == "#" or graph[position[0]][position[1]] == "$"
    )


def position_is_edge(graph, position):
    return (
        position[0] < 0  # left edge
        or position[1] < 0  # top edge
        or position[0] >= len(graph)  # bottom edge
        or position[1] >= len(graph[0])  # right edge
    )


def get_starting_position(input):
    """
    returns the starting position of the guard as a tuple
    (row, column)
    """
    for index, line in enumerate(input):
        if "^" in line:
            return (index, line.index("^"))
    return None


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
