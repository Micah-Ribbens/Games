from copy import deepcopy
from base.utility_functions import string_to_list, remove_indexes


def get_letter_combinations(letters, max_length):
    """returns: List of String; all the unique possible letter combinations with length max_length"""

    current_length = 0
    letter_combinations = []
    while True:
        if current_length >= max_length:
            break

        temp = deepcopy(letter_combinations)

        letter_combinations = []
        for letter in letters:
            for item in temp:
                new_letters = sorted(item + [letter])
                if not letter_combinations.__contains__(new_letters):
                    letter_combinations.append(new_letters)

        # The first time running through it must be populated with some letters
        if len(letter_combinations) == 0:
            for letter in letters:
                letter_combinations.append([letter])

        current_length += 1
        print("DONE", len(letter_combinations))

    return letter_combinations


def get_all_letter_combinations(letters, max_length):
    """returns: List of String; all the unique possible letter combinations with lengths from 0 -> max_length"""

    all_letter_combinations = []
    for x in range(max_length):
        all_letter_combinations += get_letter_combinations(letters, x + 1)

    return all_letter_combinations


def strings_have_same_chs(string1, string2):
    """returns boolean; if the string1 and string2 have all the same characters"""

    return sorted(string1) == sorted(string2)

def list_already_has_item(string_list, string):
    """returns: boolean; if the string_list has string (meaning if they share the same characters. i.e. 'dcba' is equal to 'abcd'"""

    return_value = False
    for item in string_list:
        if strings_have_same_chs(item, string):
            return_value = True

    return return_value


def remove_duplicates(string_list):
    """returns: List of String; the string_list without all the duplicates"""

    return_value = []

    for item in string_list:
        if not list_already_has_item(return_value, item):
            return_value.append(item)

    return return_value






