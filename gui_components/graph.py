from copy import deepcopy

from base.equations import LineSegment, Point
from gui_components.component import Component
from base.colors import black


class Graph(Component):
    """A component that displays a graph using x and y axis; only deals with positive numbers (at least for now)"""

    unmodified_lines = []
    colors = []
    modified_lines = []
    x_axis = None
    y_axis = None

    def __init__(self, lines, colors):
        """Initializes the object"""

        self.unmodified_lines = lines
        self.colors = colors

        for x in range(len(self.unmodified_lines)):
            self.unmodified_lines[x].color = self.colors[x]

    def run(self):
        pass

    def render(self):
        """Renders the object on the screen"""

        x_axis = LineSegment(Point(self.x_coordinate, self.bottom), Point(self.right_edge, self.bottom))
        y_axis = LineSegment(Point(self.x_coordinate, self.y_coordinate), Point(self.x_coordinate, self.bottom))

        x_axis.color, y_axis.color = black, black

        components = [x_axis, y_axis] + self.modified_lines

        for x in range(len(self.modified_lines)):
            self.modified_lines[x].color = self.colors[x]

        for component in components:
            component.render()

    def scale_lines(self):
        """Makes the lines fit onto the graph"""

        all_points = []
        self.modified_lines = deepcopy(self.unmodified_lines)

        for line in self.modified_lines:
            all_points.append(line.start_point)
            all_points.append(line.end_point)

        self.scale_points(all_points)

    def get_max_x_coordinate(self):
        """returns: double; the max x coordinate of this graph"""

        return_value = float("-inf")

        for line in self.unmodified_lines:

            if line.start_point.x_coordinate > return_value:
                return_value = line.start_point.x_coordinate

            if line.end_point.x_coordinate > return_value:
                return_value = line.end_point.x_coordinate

        return return_value

    def get_max_y_coordinate(self):
        """returns: double; the max y coordinate of this graph"""

        return_value = float("-inf")

        for line in self.unmodified_lines:
            if line.start_point.y_coordinate > return_value:
                return_value = line.start_point.y_coordinate

            if line.end_point.y_coordinate > return_value:
                return_value = line.end_point.y_coordinate

        return return_value

    def scale_points(self, points):
        """Scales the points so that the fit on the graph and of all of equal 'units'"""

        x_unit = self.length / self.get_max_x_coordinate()
        y_unit = self.height / self.get_max_y_coordinate()

        for point in points:
            point.x_coordinate = self.x_coordinate + (x_unit * point.x_coordinate)
            point.y_coordinate = self.bottom - (y_unit * point.y_coordinate)

    def number_set_dimensions(self, x_coordinate, y_coordinate, length, height):
        super().number_set_dimensions(x_coordinate, y_coordinate, length, height)
        self.scale_lines()

    def percentage_set_dimensions(self, percent_right, percent_down, percent_length, percent_height):
        super().percentage_set_dimensions(percent_right, percent_down, percent_length, percent_height)
        self.scale_lines()


