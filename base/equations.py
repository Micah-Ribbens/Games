from base.important_variables import *
from base.colors import *
from base.utility_functions import min_value, max_value, is_within_range, is_between_values
from gui_components.component import Component


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


class LineSegment(Component):
    """Uses the equation y = mx + b where m is slope and b is y_intercept"""

    slope = 0
    y_intercept = 0
    start_point = 0
    end_point = 0
    color = purple

    # If it is either a x_equals or y_equals then these will not be None
    x_equals = None
    y_equals = None
    is_vertical = False
    is_horizontal = False

    def __init__(self, start_point: Point, end_point: Point):
        """ summary: initializes the object

            params:
                start_point: Point; a point on the line (different than end_point)
                end_point: Point; a point on the line (different than point1)

            returns: None
        """
        # Added .01, so elsewhere when I am doing collisions I don't have to worry about straight lines :)
        if start_point.x_coordinate == end_point.x_coordinate:
            end_point.x_coordinate += .0000000001
            self.is_vertical = True

        if start_point.y_coordinate == end_point.y_coordinate:
            end_point.y_coordinate += .0000000001
            self.is_horizontal = True

        self.slope = (start_point.y_coordinate - end_point.y_coordinate) / (start_point.x_coordinate - end_point.x_coordinate)
        self.y_intercept = start_point.y_coordinate - self.slope * start_point.x_coordinate

        self.start_point = start_point
        self.end_point = end_point

    def render(self):
        """Renders the object"""

        line_height = 3
        pygame.draw.line(game_window.get_window(), self.color,
                                 (int(self.start_point.x_coordinate), int(self.start_point.y_coordinate) - line_height),
                                 (int(self.end_point.x_coordinate), int(self.end_point.y_coordinate) - line_height), line_height)

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

        return_value = None

        if self.is_vertical or self.is_horizontal:
            return_value = x_and_y_are_on_line

        else:
            return_value = x_and_y_are_on_line and is_within_range(self.get_y_coordinate(point.x_coordinate), point.y_coordinate, amount_can_be_off_by)
        return return_value

    def get_line_segment(game_object, objects_velocity, is_using_larger_coordinate, is_horizontal):
        """ summary: None

            params:
                game_object: GameObject; the object that is moving
                objects_velocity: double; the velocity of the game_object
                is_using_larger_coordinate: boolean; whether coordinates that are being used should be the larger coordinate
                is_horizontal; boolean; whether the line is based on the game_object's x coordinate

            returns: LineSegment; a line that is uses time as the x axis and the coordinate as the y axis
        """

        start_coordinate = game_object.right_edge if is_using_larger_coordinate else game_object.x_coordinate

        if not is_horizontal:
            start_coordinate = game_object.bottom if is_using_larger_coordinate else game_object.y_coordinate

        return LineSegment.get_line_segment_using_coordinates(start_coordinate, objects_velocity, is_using_larger_coordinate)

    def get_line_segment_using_coordinates(start_coordinate, velocity, is_increasing):
        """returns: LineSegment; a line that uses time as the x axis and the coordinates as the y axis"""

        start_point = Point(0, start_coordinate)
        total_time = 10
        displacement = total_time * velocity if is_increasing else total_time * -velocity
        end_point = Point(total_time, start_coordinate + displacement)

        return LineSegment(start_point, end_point)

    def contains_x_coordinate(self, x_coordinate, amount_off_acceptable=1):
        """returns: boolean; if this line contains the x_coordinate"""

        x_min, x_max = self.get_x_min_and_max()
        return is_between_values(x_min, x_max, x_coordinate, amount_off_acceptable)

    def __str__(self):
        return f"{self.start_point} -> {self.end_point}"

    def run(self):
        pass
