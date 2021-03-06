from base.dimensions import Dimensions
from base.utility_functions import *

from gui_components.component import Component


class GameObject(Component):
    """ Adds onto Dimensions (x and y coordinates, length, height, etc.) and adds upon that drawing,
        getting an object's x and y coordinates"""

    color = (0, 0, 250)
    name = ""
    attributes = ["x_coordinate", "y_coordinate"]
    object_type = ""

    def __init__(self, x_coordinate=0, y_coordinate=0, height=0, length=0, color=(0, 0, 0)):
        """summary: Initializes the object with the numbers (int) and color (RGB tuple) provided

            params:
                x_coordinate: int; the x_coordinate (in pixels) of the game_object
                y_coordinate: int; the y_coordinate (in pixels) of the game_object
                height: int; the height (in pixels) of the game_object
                length: int; the length (in pixels) of the game_object
                color: tuple; the (Red, Green, Blue) values of the game_object for color


            returns: None
            """

        super().__init__(x_coordinate, y_coordinate, length, height)
        self.color = color
        self.name = id(self)

    def render(self):
        """ summary: draws the game_object on to the game_window using the variables provided in __init__
            (x_coordinate, y_coordinate, length, height, and color)

            params: None
            returns: None
        """

        pygame.draw.rect(game_window.get_window(), self.color, (self.x_coordinate,
                         self.y_coordinate, self.length, self.height))

    def run(self):
        pass

    # Purely for debugging purposes; so you can see the location and size of game objects
    def __str__(self):
        """ summary: for debugging and it displays the x_coordinate, y_coordinate, length, height, bottom, and right_edge of the game_object
            params: None
            returns: None
        """

        return f"name {self.name} x {self.x_coordinate} y {self.y_coordinate} length {self.length} height {self.height} bottom {self.bottom} right_edge {self.right_edge}\n"

    def draw_in_segments(object, segments):
        """ summary: draws all the segments provided and uses the object's attributes to turn the percentages into numbers
            (percent_length would use the object's length to turn it into a number for instance)

            params: 
                object: GameObject; the game_object that is what the segments are segments of
                segments: list of Segment; the segments of the object
            
            returns: None
        """

        GameObject.render(object)
        for segment in segments:
            x_coordinate = percentage_to_number(segment.percent_right, object.length) + object.x_coordinate
            y_coordinate = percentage_to_number(segment.percent_down, object.height) + object.y_coordinate
            height = percentage_to_number(segment.percent_height, object.height)
            length = percentage_to_number(segment.percent_length, object.length)
            GameObject.render(GameObject(x_coordinate, y_coordinate, height, length, segment.color))

    def set_x_coordinate(self, x_coordinate):
        self.x_coordinate = x_coordinate

    def set_y_coordinate(self, y_coordinate):
        self.y_coordinate = y_coordinate

    def set_length(self, length):
        self.length = length

    def set_height(self, height):
        self.height = height


class Segment(Dimensions):
    """ Stores the necessary information for object to be drawn in segments- the color and values in relation to the base object"""

    color = (0, 0, 0)
    percent_down = 0
    percent_right = 0
    percent_length = 0
    percent_height = 0

    def __init__(self, **kwargs):
        """ summary: initializes all the values of the class based upon what is passed in by the key word arguments

            params:
                color: tuple; the RGB values that make up the color a tuple with three values (Red, Green, Blue)
                percent_down: int; the amount from the top of the object (either exact number or percentage)
                percent_right: int; the amount form the left of the object (either exact number or percentage)
                percent_length: int; the length of the segment (either exact number or percentage of the base object's length)
                percent_height: int; the height of the segment

            returns: None
        """

        self.color = kwargs.get("color")

        self.percent_down, self.percent_right = kwargs.get("percent_down"), kwargs.get("percent_right")

        self.percent_length, self.percent_height = kwargs.get("percent_length"), kwargs.get("percent_height")
        super().__init__(self.percent_right, self.percent_down, self.percent_length, self.percent_height)


class Ellipse(GameObject):
    """A GameObject this is elliptical"""

    is_outline = False

    def render(self):
        """ summary: Draws the ellipse onto the screen based upon these values:
            x_coordinate, y_coordinate, length, height, and color

            params: None
            returns: None
        """

        if self.is_outline:
            outline_length = self.length * .1
            outline_height = self.height * .1
            pygame.draw.ellipse(game_window.get_window(), self.color, (self.x_coordinate + outline_length,
                                self.y_coordinate + outline_height, self.length - outline_length, self.height - outline_height))

            pygame.draw.ellipse(game_window.get_window(), self.color, (self.x_coordinate,
                                self.y_coordinate, self.length, self.height))

        else:
            pygame.draw.ellipse(game_window.get_window(), self.color, (self.x_coordinate,
                                self.y_coordinate, self.length, self.height))

    def get_equation_variables(self):
        """ summary: finds the equations for this equation of an ellipse: (x - h)^2 / a^2 + (y - k)^2 / b^2 = 1
            params: None
            returns: list of int; the variables in the list in this order: [h, k, a, b]
        """

        # The numbers are based upon this ellipse equation: (x - h)^2 / a^2 + (y - k)^2 / b^2 = 1
        # x_center is the same as h and y_center is the same as k
        x_center = self.x_coordinate + self.length / 2
        y_center = self.y_coordinate + self.height / 2
        a = self.length / 2
        b = self.height / 2

        return [x_center, y_center, a, b]

    def get_y_coordinate_min_and_max(self, x_coordinate):
        """ summary: overrides the method from GameObject; finds all the min and max y_coordinate at that x_coordinate

            params:
                x_coordinate: double; the x_coordinate that is used to find the min and max y_coordinate
            
            returns: list of double; [y_coordinate min, y_coordinate max]
        """

        # This is the equation for an ellipse (x - h)^2 / a^2 + (y - k)^2 / b^2 = 1
        # The math below I did by hand to solve for the y_min and y_max
        h, k, a, b = self.get_equation_variables()

        # right_side is the right side of the equation so starting out the side with the 1 and the left_side is the other side with x, y, k, etc.
        # This will make the left_side look like (x - h)^2 / a^2 + (y - k)^2 / b^2
        x_fraction = pow(x_coordinate - h, 2) / pow(a, 2)

        # Equation now looks like (y - k)^2 / b^2 = 1 - (x - h)^2 / a^2
        right_side = 1 - x_fraction
        # Equation now looks like (y - k)^2 = (1 - (x - h)^2 / a^2) * b^2
        right_side *= pow(b, 2)

        # So there is not a rounding error where the number is something like 1E-8 causing an imaginary number error
        rounded(right_side, 7)

        # Should not happen, but if it does the game should not crash
        if right_side < 0:
            return [0, 0]


        # Since a sqrt can either be positive or negative you have to do +-
        y_min = sqrt(right_side) + k
        y_max = -sqrt(right_side) + k

        return [y_min, y_max]