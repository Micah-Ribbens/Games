from math import sqrt
from random import randint

import pygame

from base.important_variables import game_window, screen_length, screen_height, background_color
from base.utility_classes import Fraction


def change_attributes(modified_object, object, attributes):
    """ summary: modifies modified_object's attributes so they reflect the object's attributes
        (only the attributes in modified_object.attributes will be modified)

        params:
            modified_object: Object; the object which will have its properties modified
            object: Object; the object which the modified_object's attributes will reflect
            attributes: List of String; the attributes that should be modififed

        returns: None
    """
    for attribute in attributes:
        modified_object.__dict__[attribute] = object.__dict__[attribute]

    return modified_object


def percentage_to_number(percentage, percentage_of_number):
    """ summary: turns the percentage into a fraction which is multiplied by percentage_of_number

        params:
            percentage: int; the percentage (fraction * 100)
            percentage_of_number: int; the number that the percentage is of

        returns: int; the number that is gotten from the percentage (as a fraction) multiplied by percentage_of_number
    """
    return (percentage / 100) * percentage_of_number


def validate_kwargs_has_all_fields(kwargs_fields, kwargs):
    """ summary: raises an error if a kwarg field was not provided

        params:
            kwargs_fields: dictionary; the needed kwargs fields
            kwargs: dictionary: the provided kwargs fields

        returns: None
    """
    for field in kwargs_fields:
        if not kwargs.__contains__(field):
            raise ValueError(f"Field {field} was not provided for kwargs")


def render_words(message, font, **kwargs):
    """ summary: draws words onto the screen; either x_coordinate, y_coordinate, and text_is_center
        must be provided or is_center_of_screen

        params:
            x_coordinate: int; the x_coordinate of the text
            y_coordinate: int; the y_coordinate of the text
            is_center: boolean; the x and y coordinates are the center of the text (if True) otherwise start of text
            is_center_of_screen: boolean; the text is in the center of the screen
            text_color (optional): tuple; the (Red, Green, Blue) values of text color; is (255, 255, 255) if not specified
            text_background (optional) tuple; the (Red, Green, Blue) values of the background of the text; is background_color if not specified

        returns: None
    """

    # Getting all the variables
    text_color = (255, 255, 255) if not kwargs.get("text_color") else kwargs.get("text_color")
    text_background = background_color if not kwargs.get("text_background") else kwargs.get("text_background")
    is_center_of_screen = False if not kwargs.get("is_center_of_screen") else kwargs.get("is_center_of_screen")
    is_center = False if not kwargs.get("is_center") else kwargs.get("is_center")
    text = font.render(message, True, text_color, text_background)
    text_rect = text.get_rect()

    if is_center_of_screen:
        text_rect.center = (screen_length / 2, screen_height / 2)

    else:
        validate_kwargs_has_all_fields(["x_coordinate", "y_coordinate"], kwargs)
        text_rect.left = kwargs.get("x_coordinate")
        text_rect.top = kwargs.get("y_coordinate")

    if is_center:
        text_rect.center = (kwargs.get("x_coordinate"), kwargs.get("y_coordinate"))

    game_window.get_window().blit(text, text_rect)


# length is what percent_right and percent_length are a percent of and height is what percent_down and percent_height are a percent of
def percentages_to_numbers(percent_right, percent_down, percent_length, percent_height, length, height):
    """ summary: turns the percentages into numbers

        params:
            percent_right: int; the percent it is to right (percentage of length)
            percent_down: int; the percent it is down (percentage of height)
            percent_length: int; the length (percentage of length)
            percent_height: int; the height (percentage of height)
            length: int; the number that percent_right and percent_length are based off of
            height: int; the number that percent_down

        returns: List of int; [x_coordinate, y_coordinate, length, height]
    """
    return [
        percentage_to_number(percent_right, length),
        percentage_to_number(percent_down, height),
        percentage_to_number(percent_length, length),
        percentage_to_number(percent_height, height)
    ]


def lists_share_an_item(list1, list2):
    """ summary: iterates over list1 to see if list2 contains one of those item

        params:
            list1: list; the first list (is iterated over)
            list2: list; the second list (used to check if it shares an item with list1)

        returns: boolean; if list1 and list2 share an item
    """
    return_value = False
    for item in list1:
        if list2.__contains__(item):
            return_value = True
            break

    return return_value


def remove_last_ch(string):
    """ summary: removes the last character from a string

        params:
            string: String; the string which will have its last character removed

        returns: String; the string without the last character
    """
    return string[0:len(string) - 1]


def get_kwarg_item(kwargs, key, default_value):
    """ summary: finds the kwarg item

        params:
            kwargs: dict; the **kwargs
            key: Object; the key for the item
            default_value: Object; the value that will be obtained if the kwargs doesn't contain the key

        returns: Object; kwargs.get(key) if kwargs contains the key otherwise it will return the default_value
    """

    return kwargs.get(key) if kwargs.__contains__(key) else default_value


def mod(number, divider):
    """ summary: uses 'number % divider' but keeps the sign (+ or -) of both the number and divider for the result

        params:
            number: double; n in the equation 'n % d'
            divider: double; d in the equation 'n % d'

        returns: double; 'number % divider' while keeping the sign
    """

    result = abs(number) % abs(divider)

    # If one of the numbers and not both are negative the result should be negative
    if number * divider < 0:
        result = -result

    return result


def key_is_hit(key):
    """returns: boolean; if the key has gotten pressed"""

    return pygame.key.get_pressed()[key]


def get_leftmost_object(object1, object2):
    """returns: GameObject; the object whose x coordinate is the smallest"""
    return object1 if object1.x_coordinate < object2.x_coordinate else object2


def get_rightmost_object(object1, object2):
    """returns: GameObject; the object whose x coordinate is the biggest"""
    return object1 if object1.x_coordinate > object2.x_coordinate else object2


def get_displacement(velocity, time, is_leftwards):
    """returns: double; the displacement (left is negative and right is positive"""

    distance = time * velocity
    return -distance if is_leftwards else distance


def solve_quadratic(a, b, c):
    """returns: List of double; [answer1, answer2] the answers to the quadratic
                and if the answer is an imaginary number it returns: float('nan')"""

    number_under_square_root = pow(b, 2) - 4 * a * c
    number_under_square_root = rounded(number_under_square_root, 4)

    if number_under_square_root < 0:
        return None

    square_root = sqrt(number_under_square_root)

    answer1 = (-b + square_root) / (2 * a)
    answer2 = (-b - square_root) / (2 * a)

    answers = [answer2, answer1]

    # If the answers are the same I should only return one of them
    return answers if answers[0] != answers[1] else [answers[0]]


def min_value(item1, item2):
    """returns: double; the smallest item"""

    if item1 is None:
        return item2

    if item2 is None:
        return item1

    return item1 if item1 < item2 else item2


def max_value(item1, item2):
    """returns double; the biggest item"""

    return item1 if item1 > item2 else item2


def percent_to_number(percent):
    """returns: double; the percentage as a number"""
    return percent / 100


def is_within_range(want, got, amount_can_be_off_by):
    """ summary: finds out if want is within range of upper bound and lower bound (want +- amount_can_be_off_by respectively)

        params:
            want; double; the value that is wanted
            got: double; the double that is gotten
            amount_can_be_off_by; the amount that got can differ from want

        returns: boolean; if got is within the range of got
    """

    lower_bound = want - amount_can_be_off_by
    upper_bound = want + amount_can_be_off_by

    return got >= lower_bound and got <= upper_bound


def is_between_values(min_value, max_value, got, amount_can_be_off_by):
    """ summary: finds out if want is above min_value and below max_value (can be off by +- amount_can_be_off_by)

        params:
            min_value: double; the minimum value- must be above this value (can be off by amount_can_be_off_by)
            max_value: double; the maximum value- must be below this value (can be off amount_can_be_off_by)
            amount_can_be_off_by: double; the amount it can be off from min_value and max_value

        returns: boolean; if got is within the range of got
    """

    # Reassigning these variables using percent_error_acceptable
    min_value = min_value - amount_can_be_off_by
    max_value = max_value + amount_can_be_off_by

    return got >= min_value and got <= max_value


def get_distance(point1, point2):
    """returns: double; the distance from point1 -> point2; uses formula d = sqrt((x1 - x2)^2 + (y1 - y2)^2))"""

    return sqrt(pow(point1.x_coordinate - point2.x_coordinate, 2) + pow(point1.y_coordinate - point2.y_coordinate, 2))


def values_are_equal(object1, object2, attributes):
    """returns: boolean; if object1 and object2 have the same value for the attributes"""

    return_value = True
    for attribute in attributes:
        if object1.__dict__[attribute] != object2.__dict__[attribute]:
            return_value = False

    return return_value


def rounded(number, places):
    """returns: double; the number rounded to that many decimal places"""

    rounded_number = int(number * pow(10, places))

    # Converting it back to the proper decimals once it gets rounded from above
    return rounded_number / pow(10, places)


def get_next_index(current_index, max_index):
    next_index = current_index + 1
    return next_index if next_index <= max_index else 0


def get_prev_index(current_index, max_index):
    prev_index = current_index - 1

    return prev_index if prev_index > 0 else max_index


def get_index_of_range(ranges, number):
    """returns: int; the index of the range that has that number"""

    return_value = -1
    for x in range(len(ranges)):
        if ranges[x].__contains__(number):
            return_value = x

    return return_value


def get_min_list_item(items):
    """returns: double; the minimum item in the list"""

    min_item = float('inf')

    for item in items:
        if item < min_item:
            min_item = item

    return min_item if min_item != float('inf') else 0


def is_random_chance(probability: Fraction):
    """ summary: uses the probability for the random chance (for instance if the probability is 7/10 then 7 out of 10
        times it will return True and the other 3 times it will return False)

        params:
            probability: Fraction; the probability this function will return True

        returns: boolean; if the random number between 1-probability.denominator is >= probability.numerator
    """

    return randint(probability.numerator, probability.denominator) <= probability.numerator


def string_to_list(string):
    """returns: List of String; the string as a list"""

    string_list = []
    for ch in string:
        string_list.append(ch)

    return string_list


def list_to_string(string_list):
    "returns: String; the list as a string"

    string = ""
    for item in string_list:
        string += item

    return string


def get_uppercase(letters):
    """returns: String; the uppercase form of the letters"""

    return_value = ""

    for letter in letters:
        return_value += letter.upper()

    return return_value


def get_lowercase(letters):
    """returns: String; the lowercase form of all the letters"""

    return_value = ""

    for letter in letters:
        return_value += letter.lower()

    return return_value


def remove_indexes(letters, remove_index):
    """returns: List of String; the 'letters' without the index 'remove_index'"""

    return letters[:remove_index] + letters[remove_index + 1:]


def remove_letter(letters, letter):
    """returns: List of String; the 'letters' without the 'letter'"""

    return remove_indexes(letters, letters.index(letter))


def get_sublist(items, start, length):
    """returns: List; the list from start -> start + length"""

    return items[start: start + length]


def add_ch(string, ch, index):
    """returns: String; the string with the ch before at the index"""

    new_string = ""
    for x in range(len(string)):
        if x == index:
            new_string += ch

        new_string += string[x]

    return new_string


def remove_index(string, index):
    """returns: String; the string with the ch before at the index"""

    new_string = ""
    for x in range(len(string)):
        if x != index:
            new_string += string[x]

    return new_string


def key_is_hit(key):
    """returns: boolean; if the key has gotten pressed"""

    return pygame.key.get_pressed()[key]


def get_random_item(items):
    """ summary: gets a random index then returns items[index]

        params:
            items: List; the items that will have a random item returned from it

        returns: Object; a random item from the items
    """
    index = randint(0, len(items) - 1)

    return items[index]


def get_index_of_min_item(items):
    """returns: int; the index of the minimum item"""

    return items.index(get_min_list_item(items))


def get_converted_list(items, variable_name):
    """returns: Object[]; For each item in items it appends the item's variable (item.__dict__[variable_name])"""

    return_value = []

    for item in items:
        return_value.append(item.__dict__[variable_name])

    return return_value

