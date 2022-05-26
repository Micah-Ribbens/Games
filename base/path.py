from copy import deepcopy

from base.equations import LineSegment, Point
from base.utility_functions import max_value, get_leftmost_object, get_distance
from base.velocity_calculator import VelocityCalculator
from gui_components.component import Component


class PathLine:
    """Made up of two lines start y_coordinate to end y_coordinate and start bottom to end bottom"""

    y_coordinate_line: LineSegment = None
    bottom_line = None

    def __init__(self, y_coordinate_line, height):
        """ summary: initializes the object

            params:
                y_coordinate_line: LineSegment; the line from the start y_coordinate to the end y_coordinate
                height: double; the distance from the y_coordinate line to the bottom_line

            returns: None
        """
        self.y_coordinate_line = y_coordinate_line

        # The y_coordinate_line and bottom_line's y_coordinate are off by height
        self.bottom_line = LineSegment(Point(self.y_coordinate_line.start_point.x_coordinate, self.y_coordinate_line.start_point.y_coordinate + height),
                                       Point(self.y_coordinate_line.end_point.x_coordinate, self.y_coordinate_line.end_point.y_coordinate + height))


class Path(Component):
    """Stores the path of an object"""

    path_lines = []
    last_point = None
    height = 0
    length = 0
    is_leftwards = False

    def __init__(self, start_point, height, length):
        """ summary: initializes the object

            params:
                path_lines: List of PathLine; the path lines for this path

            returns: None
        """

        self.last_point = start_point
        self.path_lines = []
        self.height = height
        self.length = length

    def add_point(self, point):
        """Adds the path_line to the attribute 'path_lines'"""

        path_line = PathLine(LineSegment(self.last_point, point), self.height)
        self.path_lines.append(path_line)
        self.last_point = point

    def render(self):
        """Renders all the path lines"""
        distinct_colors = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128), (255, 255, 255), (0, 0, 0)]

        for x in range(len(self.path_lines)):
            y_coordinate_line = self.path_lines[x].y_coordinate_line
            bottom_line = self.path_lines[x].bottom_line

            y_coordinate_line.color = distinct_colors[x % 22]
            bottom_line.color = distinct_colors[x % 22]
            y_coordinate_line.render()
            bottom_line.render()

    def get_start_points(self):
        """returns: List of Point; [y_coordinate start point, bottom start point] for the first y_coordinate_line and bottom_line
        in the attribute 'path_lines'"""
        y_coordinate_point = self.path_lines[0].y_coordinate_line.start_point
        bottom_point = self.path_lines[0].bottom_line.start_point
        return [y_coordinate_point, bottom_point]

    def get_end_points(self):
        """returns: List of Point; [y_coordinate end point, bottom end point] for the last y_coordinate_line and bottom_line
        in the attribute 'path_lines'"""

        last_index = len(self.path_lines) - 1
        y_coordinate_point = self.path_lines[last_index].y_coordinate_line.end_point
        bottom_point = self.path_lines[last_index].bottom_line.end_point
        return [y_coordinate_point, bottom_point]

    def get_y_coordinate(self, x_coordinate):
        """returns: double; the y_coordinate at that x_coordinate"""

        for path_line in self.path_lines:
            start_point = path_line.y_coordinate_line.start_point
            end_point = path_line.y_coordinate_line.end_point

            # TODO fix so it works for both a leftwards and a rightwards path
            if x_coordinate >= start_point.x_coordinate and x_coordinate <= end_point.x_coordinate:
                return path_line.y_coordinate_line.get_y_coordinate(x_coordinate)

        return -1

    def __str__(self):
        string = ""
        for x in range(len(self.path_lines)):
            string += f"{self.path_lines[x].y_coordinate_line}\n"

        return string

    def get_lines(self):
        lines = []

        for path_line in self.path_lines:
            y_line = path_line.y_coordinate_line
            bottom_line = path_line.bottom_line

            lines.append(y_line)
            lines.append(bottom_line)

            lines.append(LineSegment(y_line.start_point, bottom_line.start_point))
            lines.append(LineSegment(y_line.end_point, bottom_line.end_point))

        return lines

    def run(self):
        pass

    def get_coordinates(self, times, line_type, coordinate_type):
        """summary: finds the coordinates of the specified type using the line_type and coordinate_type

            params:
                times: Double[]; the times at each transition of the path
                line_type: String; either 'y_coordinate_line' or 'bottom_line'
                coordinate_type: String; either 'x_coordinate' or 'y_coordinate'

            returns: SimplePath; the coordinates in relation to time
        """

        return_value = SimplePath()
        for x in range(len(self.path_lines)):
            line = self.path_lines[x].__dict__[line_type]
            time = times[x]

            return_value.add_point(Point(time, line.start_point.__dict__[coordinate_type]))

        last_line = self.path_lines[len(self.path_lines) - 1].__dict__[line_type]
        last_time = times[len(times) - 1]
        return_value.add_point(Point(last_time, last_line.end_point.__dict__[coordinate_type]))

class SimplePath:
    """A simple path that doesn't care about length or height of the object"""

    lines = []
    last_point = None

    def __init__(self, start_point=None):
        """Initializes the object"""

        self.last_point = start_point
        self.lines = []

    def add_point(self, point):
        """Adds the point to this path"""

        if self.last_point is not None:
            self.lines.append(LineSegment(self.last_point, point))
            self.last_point = point

        else:
            self.last_point = point

    def get_lines(self):
        """returns: List of LineSegment; the lines of this simple path"""

        return self.lines

    def get_first_line(self):
        """returns: Point; the first point of the simple path"""

        return self.get_lines()[0]

    def get_last_line(self):
        """returns: Point; the last point of the simple path"""

        last_index = len(self.get_lines()) - 1
        return self.get_lines()[last_index]

    def get_y_coordinate(self, x_coordinate):
        """returns: double; the y_coordinate at that x_coordinate (MUST be a function though- one x to one y)"""

        return_value = None

        for line in self.lines:
            if line.contains_x_coordinate(x_coordinate):
                return_value = line.get_y_coordinate(x_coordinate)
                break

        return return_value

    def __str__(self):
        string = ""
        for x in range(len(self.lines)):
            string += f"{self.lines[x]} || "

        return string

    def is_moving_down(self, x_coordinate):
        """returns: boolean; if the slope is negative at this point"""

        return_value = None

        for line in self.lines:
            if line.contains_x_coordinate(x_coordinate):
                return_value = not line.slope_is_positive()

        return return_value


class VelocityPath(Path):
    """A path that takes into account velocity"""

    velocity = 0
    x_coordinate_lines = []
    y_coordinate_lines = []
    last_end_time = 0

    times = []  # Stores the times that the get_coordinates() function was called
    total_time = 0
    last_point = None
    is_unending = False
    prev_time = 0

    def __init__(self, start_point, other_points, velocity):
        """Initializes the object"""

        self.velocity = velocity
        self.path_lines = []
        self.x_coordinate_lines = []
        self.y_coordinate_lines = []

        self.last_point = start_point

        for point in other_points:
            self.add_point(point)

    def add_point(self, point):
        """Does some calculations to find the time from the start of the last point to the end of the parameter 'point'
        and then calls add_time_point() to add the point"""
        x_distance = abs(self.last_point.x_coordinate - point.x_coordinate)
        y_distance = abs(self.last_point.y_coordinate - point.y_coordinate)

        end_time = max_value(x_distance / self.velocity, y_distance / self.velocity) + self.last_end_time
        self.add_time_point(point, end_time)

    def add_time_point(self, point, end_time):
        """Adds the point to the path using the end_time as the x_coordinate for the x and y coordinate lines"""
        x_coordinate_line = LineSegment(Point(self.last_end_time, self.last_point.x_coordinate),
                                        Point(end_time, point.x_coordinate))

        y_coordinate_line = LineSegment(Point(self.last_end_time, self.last_point.y_coordinate),
                                        Point(end_time, point.y_coordinate))

        self.x_coordinate_lines.append(x_coordinate_line)
        self.y_coordinate_lines.append(y_coordinate_line)
        self.last_end_time = end_time

        # The height for the path_line doesn't matter
        path_line = PathLine(LineSegment(self.last_point, point), 0)
        self.path_lines.append(path_line)

        self.last_point = point

    def get_coordinates(self):
        """returns: [x_coordinate, y_coordinate] for that time"""

        if self.prev_time != VelocityCalculator.time:
            self.total_time += VelocityCalculator.time
            self.prev_time = VelocityCalculator.time

        max_time = self.last_end_time

        if self.total_time > max_time and self.is_unending:
            self.total_time %= max_time

        return self._get_coordinates(self.total_time)

    def _get_coordinates(self, time):
        # By default it starts out as the end of the path and if the time falls within the path uses those coordinates
        last_index = len(self.x_coordinate_lines) - 1
        end_x_coordinate = self.x_coordinate_lines[last_index].end_point.y_coordinate
        end_y_coordinate = self.y_coordinate_lines[last_index].end_point.y_coordinate
        coordinates = [end_x_coordinate, end_y_coordinate]

        for x in range(len(self.y_coordinate_lines)):
            y_coordinate_line: LineSegment = self.y_coordinate_lines[x]
            x_coordinate_line: LineSegment = self.x_coordinate_lines[x]
            start_point = y_coordinate_line.start_point
            end_point = y_coordinate_line.end_point

            if time >= start_point.x_coordinate and time <= end_point.x_coordinate:
                coordinates = [x_coordinate_line.get_y_coordinate(time), y_coordinate_line.get_y_coordinate(time)]

        return coordinates

    def set_time(self, time):
        """Sets the time to the provided 'time'- if it is greater than the max time it is reduced to a smaller time"""

        self.total_time = time % self.max_time

    @property
    def max_time(self):
        return self.last_end_time

    def __str__(self):
        string = ""
        for x in range(len(self.y_coordinate_lines)):
            y_coordinate_line = self.y_coordinate_lines[x]
            x_coordinate_line = self.x_coordinate_lines[x]

            string += f"x {x_coordinate_line}, y {y_coordinate_line}\n"

        return string

    @staticmethod
    def get_paths_from_path(path, times):
        """returns: List of SimplePath; [x_coordinate_line, right_edge_line, y_coordinate_line, bottom_line]"""

        paths = VelocityPath.get_paths_list()

        elapsed_times = [0] + times # Putting a zero in the front because the first start point must be at zero otherwise it wont be

        for x in range(len(times)):
            path_line: PathLine = path.path_lines[x].y_coordinate_line

            # TODO figure out if this is sound logic :)
            VelocityPath.add_point_to_paths(paths, elapsed_times[x], path_line.start_point, path.length, path.height)

        last_path_line = path.path_lines[len(path.path_lines) - 1].y_coordinate_line
        last_time = times[len(times) - 1]

        # Have to add the end point of the last path line because it gets skipped otherwise (only use start points)
        VelocityPath.add_point_to_paths(paths, last_time, last_path_line.end_point, path.length, path.height)
        return paths

    @staticmethod
    def get_paths_list():
        """returns: List of SimplePath[4]; a list of simple path each with their own location in memory"""

        number_of_paths = 4
        return_value = []

        for x in range(number_of_paths):
            return_value.append(SimplePath())

        return return_value

    def get_paths(self, length, height, total_time):
        """returns: List of SimplePath; [x_coordinate_line, right_edge_line, y_coordinate_line, bottom_line]"""

        paths = VelocityPath.get_paths_list()
        important_times, elapsed_times = self._get_times_data(total_time)

        for x in range(len(important_times)):
            x_coordinate, y_coordinate = self._get_coordinates(important_times[x])

            VelocityPath.add_point_to_paths(paths, elapsed_times[x], Point(x_coordinate, y_coordinate), length, height)

        return paths

    def _get_times_data(self, total_time):
        """ summary: Finds the important_times and elapsed_times which are complementary to each other. The important times
            are the times that are important for the path (where it changes direction) and elapsed times is the time that
            has elapsed relative to the start (whereas important times are in relation to the time of the path checkpoints)

            returns: Double[][]; [important_times, elapsed_times]"""

        important_times = [self.total_time]
        elapsed_times = [0]
        time_left = total_time
        current_time = self.total_time
        total_elapsed_time = 0

        has_found_range = False # Whether the range that contains self.total_time has been found
        previous_time = self.total_time

        while time_left != 0:
            for y_coordinate_line in self.y_coordinate_lines:
                start_time = y_coordinate_line.start_point.x_coordinate
                end_time = y_coordinate_line.end_point.x_coordinate
                line_time = end_time - previous_time

                is_within_range = self.total_time >= start_time and self.total_time <= end_time
                if not is_within_range and not has_found_range:
                    previous_time = end_time
                    continue

                else:
                    has_found_range = True

                if line_time >= time_left:
                    total_elapsed_time += time_left
                    important_times.append(current_time + time_left)
                    time_left = 0

                else:
                    important_times.append(current_time + line_time)
                    current_time = end_time
                    time_left -= line_time
                    total_elapsed_time += line_time

                elapsed_times.append(total_elapsed_time)
                previous_time = end_time

        return [important_times, elapsed_times]


    @staticmethod
    def add_point_to_paths(paths, current_time, point, length, height):
        """Adds the points to the path; NOTE: paths must be a list like this: [x coordinate line, right edge line,
            y coordinate line, bottom line]"""

        # x coordinate line
        paths[0].add_point(Point(current_time, point.x_coordinate))

        # right edge line
        paths[1].add_point(Point(current_time, point.x_coordinate + length))

        # y coordinate line
        paths[2].add_point(Point(current_time, point.y_coordinate))

        # bottom line
        paths[3].add_point(Point(current_time, point.y_coordinate + height))















class ObjectPath(Path):
    """A Path that is specifically for tracking an object from one point to another"""

    prev_object = None
    current_object = None
    is_runnable = False

    def __init__(self, prev_object, current_object):
        """initializes the object; does the path that covers the most area of the object"""

        is_moving_leftwards = get_leftmost_object(prev_object, current_object) == current_object

        if is_moving_leftwards:
            super().__init__(Point(prev_object.right_edge, prev_object.y_coordinate), prev_object.height, prev_object.length)
            self.add_point(Point(current_object.x_coordinate, current_object.y_coordinate))

        else:
            super().__init__(Point(prev_object.x_coordinate, prev_object.y_coordinate), prev_object.height, prev_object.length)
            self.add_point(Point(current_object.right_edge, current_object.y_coordinate))

        self.is_leftwards = is_moving_leftwards
        self.prev_object = prev_object
        self.current_object = current_object

    def get_time_lines(self):
        """ summary: gets all the lines in the path; all the lines are in relation to time: 0 -> VelocityCalculator.time

            params: None

            returns: List of Line; [x_coordinate_line, right_edge_line, y_coordinate_line, bottom_line]
        """

        x_coordinate_line = self._get_time_line(self.prev_object.x_coordinate, self.current_object.x_coordinate)
        right_edge_line = self._get_time_line(self.prev_object.right_edge, self.current_object.right_edge)
        y_coordinate_line = self._get_time_line(self.prev_object.y_coordinate, self.current_object.y_coordinate)
        bottom_line = self._get_time_line(self.prev_object.bottom, self.current_object.bottom)
        return [x_coordinate_line, right_edge_line, y_coordinate_line, bottom_line]

    def _get_time_line(self, start_coordinate, end_coordinate):
        """ returns: LineSegment; a line that has time as the x coordinate and the y coordinate is the coordinates
            provided in the parameters"""

        return LineSegment(Point(0, start_coordinate), Point(VelocityCalculator.time, end_coordinate))

    def get_start_point(self):
        """returns: Point; the start point of the object"""

        return Point(self.prev_object.x_coordinate, self.prev_object.y_coordinate)

    def get_xy_point(self, line, point):
        line_is_rightwards = line.start_point.x_coordinate < line.end_point.x_coordinate
        is_bottom_line = line.start_point.y_coordinate == self.prev_object.bottom
        xy_point = deepcopy(point)

        if line_is_rightwards:
            # The end point of the line if it is the current_object's right_edge, so substracting the length gets the x cooordinate
            xy_point.x_coordinate -= self.length

        if is_bottom_line:
            # The line is based off the bottom, so subtracting the height gets the y coordinate
            xy_point.y_coordinate -= self.height

        return xy_point

    def get_end_point(self):
        """returns: Point; the end point of the object"""
        return Point(self.current_object.x_coordinate, self.current_object.y_coordinate)

    def get_total_distance(self):
        """returns: double; the total amonut of distance the object has traveled"""
        return get_distance(self.get_start_point(), self.get_end_point())

    def get_lines(self):
        """returns: List of LineSegment; the lines of the object path"""

        return [
            LineSegment(Point(self.prev_object.x_coordinate, self.prev_object.y_coordinate), Point(self.current_object.x_coordinate, self.current_object.y_coordinate)),
            LineSegment(Point(self.prev_object.right_edge, self.prev_object.y_coordinate), Point(self.current_object.right_edge, self.current_object.y_coordinate)),
            LineSegment(Point(self.prev_object.right_edge, self.prev_object.bottom), Point(self.current_object.right_edge, self.current_object.bottom)),
            LineSegment(Point(self.prev_object.x_coordinate, self.prev_object.bottom), Point(self.current_object.x_coordinate, self.current_object.bottom)),
        ]

    def get_x_distance(self):
        """returns: double; the x distance of the line"""
        return abs(self.path_line.end_point - self.path_line.start_point.x_coordinate)

    @property
    def path_line(self):
        """returns: PathLine; the only path_line since it is an object path"""

        return self.path_lines[0].y_coordinate_line





