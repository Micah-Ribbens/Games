from copy import deepcopy
from math import pow

from base.velocity_calculator import VelocityCalculator


class HistoryKeeperObject:
    object = None
    time = 0
    """HistoryKeeper uses the class to store its object"""

    def __init__(self, object_being_stored):
        """ summary: initializes the HistoryKeeperObject,
            so its attributes reflects what is passed through the parameters
            params:
                object: Object; the object that is being stored
            returns: None
        """

        self.object = object_being_stored
        self.time = VelocityCalculator.time


class HistoryKeeper:
    """Stores the values of past objects"""

    last_objects = {}
    times = []
    last_time = 0

    def reset():
        """ summary: resets the HistoryKeeper, so it has no more values of past objects
            params: None
            returns: None
        """

        HistoryKeeper.last_objects = {}
        HistoryKeeper.times = []

    def add(object, name, is_game_object):
        """ summary: adds the object to the HistoryKeeper; IMPORTANT: make sure to provide a unique name for each unique object!
            params:
                object: Object; the object that is going to be added to the HistoryKeeper
                name: String; the unique name (identifier) for the object
                is_game_object: boolean; the object provided is an instance of GameObject
            returns: None
        """

        # Have to deepcopy the object if it is a GameObject so it is in a different place in memory
        # So if the GameObject's values change the HistoryKeeper's one doesn't also change
        if is_game_object:
            object = deepcopy(object)

        HistoryKeeper.last_objects[f"{name}{VelocityCalculator.time}"] = object

    def get_last(name):
        """ summary: gets the version of that object from the last cycle
            params:
                name: String; the unique name (identifier) given for the object in HistoryKeeper.add() that is used to retrieve the previous version of the object
            returns: the version of the object from the last cycle
        """

        return HistoryKeeper.last_objects.get(f"{name}{HistoryKeeper.last_time}")

    def get_last_time():
        """ summary: gets the time from the last cycle
            params: None
            returns: the time from the last cycle
        """
        last_time = 0
        for x in range(len(HistoryKeeper.times)):
            # Length and last index are off by one, so have to minus one to not get a IndexError
            time = HistoryKeeper.times[len(HistoryKeeper.times) - 1 - x]
            # Meaning we found the last time since we are iterating over all cycle times backwards
            if time != VelocityCalculator.time:
                last_time = time
                break

        return last_time


class Fraction:
    """Has a numerator and a denominator along with utility functions that go along with fractions"""
    numerator = None
    denominator = None

    def __init__(self, numerator, denominator):
        """ summary: initializes the fraction
            params:
                numerator: int; the top part of the fraction
                denominator: int; the bottom part of the fraction
            returns: None
        """
        self.numerator = numerator
        self.denominator = denominator

    def get_reciprocal(self):
        """ summary: In math reciprocal is denominator/numerator
            params: None
            returns: Fraction; a new Fraction where the denominator and numerator switch places
        """
        return Fraction(self.denominator, self.numerator)

    def get_number(self):
        """ summary: turns the fraction into a number
            params: None
            returns: float; the
        """
        return self.numerator / self.denominator

    def get_fraction_to_power(self, power):
        """ summary: uses the function pow() to get the fraction to the specified power
            params:
                power: int; the power to which the fraction is raised
            returns: Fraction; a new fraction where the numerator and denominator are raised to the power specified
        """
        return Fraction(pow(self.numerator, power), pow(self.denominator, power))

    # Gets the other part of the fraction to make it one
    # For instance for 3/4 it would do 4 - 3/4 which would be 1/4 and 1/4 + 3/4 = 1
    def get_fraction_to_become_one(self):
        """ summary: gets the fraction that makes the current fraction + the new fraction equal to one
            for instance if the current fraction is 3/4 then 1 - 3/4 the new fraction would be 1/4
            params: None
            returns: Fraction; a new Fraction where the current fraction + the new fraction equals one
        """
        return Fraction(self.denominator - self.numerator, self.denominator)

    def __str__(self):
        """ summary: formats the Fraction in this form "numerator/denominator"
            params: None
            returns: String; "numerator/denominator"- looks like this when printed 1/4 (if numerator was 1 and denominator was 4)
        """
        return f"{self.numerator}/{self.denominator}"


class StateChange:
    """Stores the information for changing between states"""

    condition = False
    state = 0

    def __init__(self, condition, state):
        """Initializes the object"""

        self.condition = condition
        self.state = state


class Range:
    """Stores the information for a start and end of a range"""

    start = 0
    end = 0

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_less_than(self, other_range):
        """returns: boolean; if this range's start is less than the other range's start"""
        starts_are_equal = self.start == other_range.start

        if starts_are_equal:
            return self.end < other_range.end

        else:
            return self.start < other_range.start

    def __str__(self):
        return f"{self.start} -> {self.end}"

    def __contains__(self, number):
        """returns: boolean; if the number is within the range- greater than start and less than end"""

        return number >= self.start and number <= self.end

