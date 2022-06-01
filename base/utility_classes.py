from base.drawable_objects import GameObject
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

        added_object = object

        # Have to deepcopy the object if it is a GameObject so it is in a different place in memory
        # So if the GameObject's values change the HistoryKeeper's one doesn't also change
        if is_game_object:
            added_object = GameObject(object.x_coordinate, object.y_coordinate, object.height, object.length)
            added_object.name = object.name

        HistoryKeeper.last_objects[f"{name}{VelocityCalculator.time}"] = added_object

    def get_last(name):
        """ summary: gets the version of that object from the last cycle
            params:
                name: String; the unique name (identifier) given for the object in HistoryKeeper.add() that is used to retrieve the previous version of the object
            returns: the version of the object from the last cycle
        """

        return HistoryKeeper.last_objects.get(f"{name}{HistoryKeeper.last_time}")

    def is_populated(all_objects):
        """returns: boolean; if the History Keeper has these objects in it NOTE: each object in object must have the attribute name"""

        return_value = True

        for object in all_objects:
            if HistoryKeeper.get_last(object.name) is None:
                return_value = False

        return return_value

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

