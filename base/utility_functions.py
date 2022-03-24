from math import sqrt

import pygame

from base.important_variables import game_window, screen_length, screen_height, background_color


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
    is_true = False
    for item in list1:
        if list2.__contains__(item):
            is_true = True
            break

    return is_true


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

    if number_under_square_root < 0:
        return None

    square_root = sqrt(number_under_square_root)

    answer1 = (-b + square_root) / (2 * a)
    answer2 = (-b - square_root) / (2 * a)
    return [answer2, answer1]



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


def get_index_of_range(ranges, number):
    """returns: int; the index of the range that has that number"""

    return_value = -1
    for x in range(len(ranges)):
        if ranges[x].__contains__(number):
            return_value = x

    return return_value


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
