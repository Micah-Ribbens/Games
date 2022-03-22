from base.quadratic_equations import *
from base.important_variables import *
from base.colors import *
from base.utility_functions import min_value, max_value, is_within_range, is_between_values


class Point:
    x_coordinate = 0
    y_coordinate = 0

    """Stores the x and y coordinates of point"""

    def __init__(self, x_coordinate, y_coordinate):
        """ summary: initializes the object

            params:
                x_coordinate: double; the value of the point's x coordinate
                y_coordinate: double; the value of the point's y coordinate

            returns: None
        """

        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate

    def __str__(self):
        return f"({self.x_coordinate}, {self.y_coordinate})"


class LineSegment:
    """Uses the equation y = mx + b where m is slope and b is y_intercept"""

    slope = 0
    y_intercept = 0
    start_point = 0
    end_point = 0
    color = purple

    # If it is either a x_equals or y_equals then these will not be None
    x_equals = None
    y_equals = None

    def __init__(self, start_point: Point, end_point: Point):
        """ summary: initializes the object

            params:
                start_point: Point; a point on the line (different than end_point)
                end_point: Point; a point on the line (different than point1)

            returns: None
        """
        # Added .01, so elsewhere when I am doing collisions I don't have to worry about straight lines :)
        if start_point.x_coordinate == end_point.x_coordinate:
            end_point.x_coordinate += .00000001

        if start_point.y_coordinate == end_point.y_coordinate:
            end_point.y_coordinate += .00000001

        self.slope = (start_point.y_coordinate - end_point.y_coordinate) / (start_point.x_coordinate - end_point.x_coordinate)
        self.y_intercept = start_point.y_coordinate - self.slope * start_point.x_coordinate

        self.start_point = start_point
        self.end_point = end_point

    def render(self):
        """Renders the object"""

        pygame.draw_py.draw_line(game_window.get_window(), self.color,
                                 (int(self.start_point.x_coordinate), int(self.start_point.y_coordinate)),
                                 (int(self.end_point.x_coordinate), int(self.end_point.y_coordinate)), 9)

    def get_y_coordinate(self, x_coordinate):
        """ summary: finds the y_coordinate using the equation y = mx + b

            params:
                x_coordinate: the x coordinate which will be used to find the y_coordinate

            returns: double; the y coordinate
        """

        return self.slope * x_coordinate + self.y_intercept

    def get_x_coordinate(self, y_coordinate):
        """ summary: finds the x coordinate using the equation x = (y - b) / m

            params:
                y_coordinate: the y coordinate which will be used to find the x coordinate

            returns: double; the x coordinate
        """

        return (y_coordinate - self.y_intercept) / self.slope

    def slope_is_positive(self):
        """returns: boolean; if the slope is >= 0"""

        return self.slope >= 0

    def is_x_equals_line(self):
        """returns: boolean; if the line is something like 'x = 6'"""

        return self.start_point.x_coordinate == self.end_point.x_coordinate

    def is_y_equals_line(self):
        """returns: boolean; if the line is something like 'y = 6'"""

        return self.start_point.y_coordinate == self.end_point.y_coordinate

    def get_x_min_and_max(self):
        """returns: [min x coordinate, max x coordinate]"""

        x_min = min_value(self.start_point.x_coordinate, self.end_point.x_coordinate)
        x_max = max_value(self.start_point.x_coordinate, self.end_point.x_coordinate)

        return [x_min, x_max]

    def get_y_min_and_max(self):
        """returns: [min y coordinate, max y coordinate]"""

        y_min = min_value(self.start_point.y_coordinate, self.end_point.y_coordinate)
        y_max = max_value(self.start_point.y_coordinate, self.end_point.y_coordinate)

        return [y_min, y_max]

    def contains_point(self, point: Point, amount_can_be_off_by):
        """ summary: finds out if the line contains the point (the point can differ from the line by 'percent_error_acceptable')

            params:
                point: Point; the point in question
                percent_error_acceptable: double; the amount the point can differ from the line

            returns: boolean; if the line contains the point
        """

        x_min, x_max = self.get_x_min_and_max()
        y_min, y_max = self.get_y_min_and_max()

        x_is_on_line = is_between_values(x_min, x_max, point.x_coordinate, amount_can_be_off_by)
        y_is_on_line = is_between_values(y_min, y_max, point.y_coordinate, amount_can_be_off_by)
        x_and_y_are_on_line = x_is_on_line and y_is_on_line

        return x_and_y_are_on_line and is_within_range(self.get_y_coordinate(point.x_coordinate), point.y_coordinate, amount_can_be_off_by)

    def get_line_segment(game_object, objects_velocity, is_increasing, is_horizontal):
        """ summary: None

            params:
                game_object: GameObject; the object that is moving
                objects_velocity: double; the velocity of the game_object
                is_increasing: boolean; whether the game_object's coordinates are increasing
                is_horizontal; boolean; whether the line is based on the game_object's x coordinate

            returns: LineSegment; a line that is uses time as the x axis and the coordinate as the y axis
        """

        start_coordinate = game_object.right_edge if is_increasing else game_object.x_coordinate
        if not is_horizontal:
            start_coordinate = game_object.bottom if is_increasing else game_object.y_coordinate

        # The time is the x axis and the coordinate is the y axis
        start_point = Point(0, start_coordinate)
        total_time = 10
        displacement = total_time * objects_velocity if is_increasing else -objects_velocity * total_time
        end_point = Point(total_time, start_coordinate + displacement)

        return LineSegment(start_point, end_point)

    def __str__(self):
        return f"{self.start_point} -> {self.end_point}"


class CollisionLine(LineSegment):
    is_bottom_line = False

    def __init__(self, line, is_bottom_line):
        super().__init__(line.start_point, line.end_point)

        self.is_bottom_line = is_bottom_line