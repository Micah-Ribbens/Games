from base.utility_classes import Range
from base.utility_functions import get_index_of_range
from base.velocity_calculator import VelocityCalculator
from gui_components.sub_screen import SubScreen
from gui_components.text_box import TextBox
from base.colors import *
from base.important_variables import *


class IntermediateScreens(SubScreen):
    """A class that displays a message for  period of time"""

    time_ranges = []
    screen_components = []
    current_time = 0
    max_time = 0
    is_being_displayed = False

    def __init__(self, height_used_up, length_used_up, number_of_screens):
        """Initializes the object"""

        self.screen_components, self.time_ranges = [], []

        for x in range(number_of_screens):
            text_box = TextBox("", 42, False, white, background_color)
            self.screen_components.append(text_box)
            text_box.number_set_dimensions(length_used_up, height_used_up, screen_length - length_used_up,
                                           screen_height - height_used_up)
            text_box.set_text_is_centered(True)

        super().__init__(height_used_up, length_used_up)

    def display(self, messages, times):
        """Sets up the display for the intermediate screens; NOTE the length of messages and times must match the
        'amount_of_screens' passed in __init__()"""

        current_time = 0
        self.is_being_displayed = True
        self.time_ranges = []

        for time in times:
            self.time_ranges.append(Range(current_time, current_time + time))
            current_time += time
        self.max_time = current_time

        for x in range(len(messages)):
            self.screen_components[x].text = messages[x]

    def get_components(self):
        """returns: List of Component; the components that should be displayed"""

        index = get_index_of_range(self.time_ranges, self.current_time)
        return [self.screen_components[index]]

    def reset(self):
        """Resets the object back to the start"""

        self.current_time = 0
        self.is_being_displayed = False

    def is_done(self):
        """returns: boolean; if the intermediate screens are done being displayed"""
        return self.current_time > self.max_time or not self.is_being_displayed

    def run(self):
        """Runs all the code necessary to make this object work properly"""

        self.current_time += VelocityCalculator.time
