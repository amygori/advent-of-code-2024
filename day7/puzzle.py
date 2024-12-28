import sys
from pathlib import Path
from pprint import pprint
import itertools


def do_the_thing(input):
    result = part_one(input)
    return result


def part_one(input):
    data = [line.split(":") for line in input]

    calibration_result = 0

    for nums in data:
        target_value = int(nums[0])
        nums = [int(n) for n in nums[1].lstrip().split(" ")]
        operator_count = len(nums) - 1

        for combination in generate_combinations(operator_count):
            if calculate(nums, combination) == target_value:
                calibration_result += target_value
                break

    return calibration_result


def generate_combinations(operator_count):
    """
    Generator function! yields all possible combinations of operators
    """
    operators = ["*", "+", "||"]
    for combination in itertools.product(operators, repeat=operator_count):
        yield combination


def calculate(nums, combination):
    result = nums[0]
    # Apply each operator in the combination to the corresponding numbers
    for idx, operator in enumerate(combination):
        if operator == "+":
            result += nums[idx + 1]
        elif operator == "*":
            result *= nums[idx + 1]
        elif operator == "||":
            # Concatenate the numbers on either side of the operator
            result = int(str(result) + str(nums[idx + 1]))
    return result


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
