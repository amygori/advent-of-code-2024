import sys
from pathlib import Path
from pprint import pprint


def do_the_thing(input):
    # segment the input into rules and updates
    newline = input.index("")
    rules = parse_rules(input[:newline])
    updates = input[newline + 1 :]
    res = part_two(rules, updates)
    return res


def part_two(rule_data, updates):
    # get a list of the incorrectly ordered updates
    invalid_updates = get_incorrectly_ordered_updates(rule_data, updates)
    print("Invalid updates: ", invalid_updates)


def get_incorrectly_ordered_updates(rules, updates):
    ordered_updates = []
    valid_update = True
    for update in updates:
        update = update.split(",")
        valid_update = True

        for idx in range(len(update)):
            valid = rule_check(idx, update, rules)
            if not valid:
                valid_update = False
                break  # if the update is invalid, break out of the loop
        if not valid_update:
            ordered_updates.append(update)
    return ordered_updates


def part_one(rules, updates):
    ordered_updates = []
    valid_update = True
    for update in updates:
        update = update.split(",")
        valid_update = True

        for idx in range(len(update)):
            valid = rule_check(idx, update, rules)
            if not valid:
                valid_update = False
                break  # if the update is invalid, break out of the loop
        if valid_update:
            ordered_updates.append(update)

    sum_of_middle_nums = 0
    for update in ordered_updates:
        sum_of_middle_nums += int(update[len(update) // 2])
    return sum_of_middle_nums


def rule_check(idx, update, rules, valid=False):
    idx = int(idx)
    if idx == len(update):
        return valid

    if idx == len(update) - 1:  # then it's the last num in the list
        current_page = update[idx]
        prev_page = update[idx - 1]
    else:
        current_page = update[idx + 1]
        prev_page = update[idx]
    try:  # is there a rule that says the current page can follow the previous page?
        valid = current_page in rules["pages_that_follow"][prev_page]
    except KeyError:
        valid = True  # if there is no rule, then it's valid
    try:  # is there a rule that says the previous page should come after the current page?
        valid = prev_page not in rules["pages_that_follow"][current_page]
    except KeyError:
        valid = True
    if not valid:
        return valid
    return rule_check(idx + 1, update, rules, valid)


def parse_rules(rules):
    # parse the rules into a dictionary
    # look up the key to find the numbers that should come after it.
    # after lists the values that must come after the key -- the key comes before the values that are listed for it
    rules_dict = {"pages_that_follow": {}, "pages_that_precede": {}}
    for rule in rules:
        rule = rule.split("|")
        try:
            rules_dict["pages_that_follow"][rule[0]].append(rule[1])
        except KeyError:
            rules_dict["pages_that_follow"][rule[0]] = []
            rules_dict["pages_that_follow"][rule[0]].append(rule[1])
        try:  # in case I want to look it up this way
            rules_dict["pages_that_precede"][rule[1]].append(rule[0])
        except KeyError:
            rules_dict["pages_that_precede"][rule[1]] = []
            rules_dict["pages_that_precede"][rule[1]].append(rule[0])
    return rules_dict


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
