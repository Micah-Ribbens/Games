from abc import ABC, abstractmethod

from base.important_variables import screen_length, screen_height
from base.utility_functions import percentage_to_number, percentages_to_numbers
from base.dimensions import Dimensions


class Component(ABC, Dimensions):
    """The components that are added to the game's window"""

    is_visible = True
    is_runnable = True
    is_selected = False

    @abstractmethod
    def run(self):
        pass
    
    @abstractmethod
    def render(self):
        pass

    def percentage_set_dimensions(self, percent_right, percent_down, percent_length, percent_height):
        """ summary: sets the component's dimensions based on the values passed into this function (calls percentages_to_numbers)
            
            params:
                percent_right: int; the percent it is to right (percentage of screen_length)
                percent_down: int; the percent it is down (percentage of screen_height)
                percent_length: int; the length (percentage of screen_length)
                percent_height: int; the height (percentage of screen_height)
            returns: None
        """
        # numbers = percentages_to_numbers(percent_right, percent_down, percent_length, percent_height, screen_length, screen_height)
        # self.x_coordinate, self.y_coordinate, self.length, self.height = numbers
        self.x_coordinate = percentage_to_number(percent_right, screen_length)
        self.y_coordinate = percentage_to_number(percent_down, screen_height)
        self.length = percentage_to_number(percent_length, screen_length)
        self.height = percentage_to_number(percent_height, screen_height)

    def number_set_dimensions(self, x_coordinate, y_coordinate, length, height):
        """ summary: sets the component's dimensions based on the values passed into this function

            params:
                x_coordinate: int; the new x coordinate of the component
                y_coordinate: int; the new y coordinate of the component
                length: int; the new length of the component
                height: int; the new height of the component

            returns: None
        """
        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate
        self.length, self.height = length, height

    def set_dimensions(self, dimensions):
        """ summary: sets the object's dimensions to the dimension's of the parameter dimensions

            params:
                dimensions: Dimension; the dimensions that this object should be

            returns: None
        """
        self.x_coordinate = dimensions.x_coordinate
        self.y_coordinate = dimensions.y_coordinate
        self.length = dimensions.length
        self.height = dimensions.height
