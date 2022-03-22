class Dimensions:
    """Gives x_coordinate, y_coordinate, height, length and then using those number it provides
    right_edge, bottom, x_midpoint, and y_midpoint"""

    x_coordinate = 0
    y_coordinate = 0
    length = 0
    height = 0

    def __init__(self, x_coordinate, y_coordinate, length, height):
        """ summary: Initializes all the attributes of the class with the numbers provided

            params:
                x_coordinate: int; the x_coordinate of the object
                y_coordinate: int; the y_coordinate of the object
                length: int; the length of the object
                height: int; the height of the object

            returns: None
        """

        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate
        self.length, self.height = length, height

    # @property automatically changes this "attribute" when the x_coordinate or length changes
    # Can be treated as an attribute
    @property
    def right_edge(self):
        """The x_coordinate + length is what constitutes the object's right_edge"""

        return self.x_coordinate + self.length

    @property
    def bottom(self):
        """The y_coordinate + height is what constitutes the object's bottom"""

        return self.y_coordinate + self.height

    @property
    def x_midpoint(self):
        """The x_coordinate + length / 2 is what constitutes the object's x_midpoint"""
        return self.x_coordinate + self.length / 2

    @property
    def y_midpoint(self):
        """The y_coordinate + height / 2 is what constitutes the object's y_midpoint"""

        return self.y_coordinate + self.height / 2