from math import sqrt

from base.drawable_objects import GameObject, Ellipse
from base.equations import Point, LineSegment
from base.path import Path, ObjectPath, SimplePath
from base.utility_classes import HistoryKeeper, Range
from base.important_variables import (
    screen_height,
    screen_length
)
from base.utility_functions import get_rightmost_object, get_leftmost_object, max_value, get_distance, \
    values_are_equal
from base.utility_functions import lists_share_an_item, solve_quadratic, min_value, is_within_range
from base.velocity_calculator import VelocityCalculator


class CollisionData:
    """Stores all the data for collisions"""
    is_collision = False
    is_moving_collision = False
    is_moving_right_collision = False
    is_moving_left_collision = False
    object_xy = None

    def __init__(self, is_collision, is_moving_collision, is_moving_right_collision, is_moving_left_collision, object_xy):
        self.is_collision, self.is_moving_collision = is_collision, is_moving_collision
        self.is_moving_right_collision, self.is_moving_left_collision = is_moving_right_collision, is_moving_left_collision
        self.object_xy = object_xy


class CollisionsUtilityFunctions:
    point_deviation_allowed = pow(10, -7) # The amount a suggested collision point and a point on the actual line can deviate

    def get_object_xy(current_object, prev_object, time):
        """returns: Point; the object's x and y at that time"""

        x_line = LineSegment(Point(0, prev_object.x_coordinate), Point(VelocityCalculator.time, current_object.x_coordinate))
        y_line = LineSegment(Point(0, prev_object.y_coordinate), Point(VelocityCalculator.time, current_object.y_coordinate))
        return Point(x_line.get_y_coordinate(time), y_line.get_y_coordinate(time))

    def get_is_right_collision(object1_x_displacement, object2_x_displacement):
        """ summary: uses the displacements to find out if it is a right collision

            params:
                object1_x_displacement: double; the displacement of the object in question to see if it hit/got hit object2 from the right
                object2_x_displacement: double; the displacement of the other object

            returns: boolean; if object1 hit/ got hit by object2 from the right
        """
        is_moving_right_collision = False

        object1_x_distance_traveled = abs(object1_x_displacement)
        object2_x_distance_traveled = abs(object2_x_displacement)

        if object2_x_distance_traveled >= object1_x_distance_traveled:
            # Since object2 traveled a greater distance its displacement matters more (if it goes leftwards into the ball
            # it would be a left collision and if it goes rightwards it would be a right collision)
            is_moving_right_collision = object2_x_displacement > 0

        else:
            # Otherwise, since object1 has traveled the greater distance the direction it goes matters most
            is_moving_right_collision = object1_x_displacement < 0

        return is_moving_right_collision

    def get_collision_data(object1, object2, collision_time, is_moving_collision):
        """returns: List of CollisionData; [object1 Collision Data, object2 Collision Data]"""

        is_collision = collision_time != -1

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)
        object1_displacement = object1.x_coordinate - prev_object1.x_coordinate
        object2_displacement = object2.x_coordinate - prev_object2.x_coordinate
        object_xy = CollisionsUtilityFunctions.get_object_xy(object1, prev_object1, collision_time)
        is_moving_right_collision = CollisionsUtilityFunctions.get_is_right_collision(object1_displacement, object2_displacement)
        is_moving_left_collision = not is_moving_right_collision

        return CollisionData(is_collision, is_moving_collision, is_moving_right_collision, is_moving_left_collision, object_xy)

    def get_path_collision_time(object1_path, object2_path):
        """ summary: finds the time that object1 and object2 collide using their paths

            params:
                object1_paths: List of Path; [object1 x path, object1 right edge path]- the path of object1


            returns: List of Collision; [object1 CollisionData, object2 CollisionData]"""

        x_line1, right_edge_line1, y_line1, bottom_line1 = object1_path.get_time_lines()
        x_line2, right_edge_line2, y_line2, bottom_line2 = object2_path.get_time_lines()

        x_ranges = [CollisionsUtilityFunctions.get_times_between(x_line1, x_line2, right_edge_line2),
                    CollisionsUtilityFunctions.get_times_between(right_edge_line1, x_line2, right_edge_line2),
                    CollisionsUtilityFunctions.get_times_between(x_line2, x_line1, right_edge_line1),
                    CollisionsUtilityFunctions.get_times_between(right_edge_line2, x_line1, right_edge_line1)]

        y_ranges = [CollisionsUtilityFunctions.get_times_between(y_line1, y_line2, bottom_line2),
                    CollisionsUtilityFunctions.get_times_between(bottom_line1, y_line2, bottom_line2),
                    CollisionsUtilityFunctions.get_times_between(y_line2, y_line1, bottom_line1),
                    CollisionsUtilityFunctions.get_times_between(bottom_line2, y_line1, bottom_line1)]

        x_ranges = CollisionsUtilityFunctions.filter_ranges(x_ranges)
        y_ranges = CollisionsUtilityFunctions.filter_ranges(y_ranges)
        return_value = float('inf')
        prev_object1, current_object1 = object1_path.prev_object, object1_path.current_object
        prev_object2, current_object2 = object2_path.prev_object, object2_path.current_object

        for x_range in x_ranges:
            y_and_bottom_equal = (prev_object1.y_coordinate == prev_object2.y_coordinate and
                                  current_object1.bottom == current_object2.bottom)

            x_and_right_edge_equal = (prev_object1.x_coordinate == prev_object2.x_coordinate
                                      and current_object1.right_edge == current_object2.right_edge)

            if y_and_bottom_equal:
                return_value = x_range.start if x_range.start < return_value else return_value

            for y_range in y_ranges:
                if x_and_right_edge_equal:
                    return_value = y_range.start if y_range.start < return_value else return_value

                smaller_range = x_range if x_range.is_less_than(y_range) else y_range
                bigger_range = x_range if not x_range.is_less_than(y_range) else y_range
                # Meaning that the ranges share a similar point
                if smaller_range.end >= bigger_range.start and bigger_range.start < return_value:
                    time = bigger_range.start
                    return_value = time if time < return_value else return_value

        return return_value if return_value != float('inf') else -1

    def filter_ranges(ranges):
        """summary: deletes all the ranges that are from 0 to 0 (0 -> 0)"""

        return_value = []
        for x in range(len(ranges)):
            ranges_are_positive = ranges[x].start < 0 and ranges[x].end < 0
            if not (ranges[x].start == 0 and ranges[x].end == 0) and not ranges_are_positive:
                return_value.append(ranges[x])
        return return_value

    def is_between_lines(line, bottom_line, top_line, is_testing_end_points):
        """returns: boolean; if the line's end or start point are between the bottom_line's and top_line's end or start point"""
        if is_testing_end_points:
            return (line.end_point.y_coordinate >= bottom_line.end_point.y_coordinate and
                    line.end_point.y_coordinate <= top_line.end_point.y_coordinate)
        else:
            return (line.start_point.y_coordinate >= bottom_line.start_point.y_coordinate and
                    line.start_point.y_coordinate <= top_line.start_point.y_coordinate)

    def get_times_between(line: LineSegment, bottom_line: LineSegment, top_line: LineSegment):
        """returns: List of Range; the times that 'line' is between 'top_line' and 'bottom_line' NOTE: the lines must have
        time as their x coordinate and the coordinates (x, y, bottom, or right_edge) as the y coordinate"""

        is_between_lines = CollisionsUtilityFunctions.is_between_lines(line, bottom_line, top_line, False)

        collision_times = []
        time1 = CollisionsUtilityFunctions.get_line_collision_point(line, top_line)
        time2 = CollisionsUtilityFunctions.get_line_collision_point(line, bottom_line)

        # Adding the time1 and time2 to collision_times if there was a collision: -1
        collision_times += [time1.x_coordinate] if time1 is not None else []
        collision_times += [time2.x_coordinate] if time2 is not None else []

        collision_times.sort()
        collision_times = list(filter(lambda item: item != 0, collision_times))

        start_time = 0

        return_value = None
        for collision_time in collision_times:
            if is_between_lines:
                return_value = Range(start_time, collision_time)

            is_between_lines = not is_between_lines
            start_time = collision_time

        if is_between_lines and CollisionsUtilityFunctions.is_between_lines(line, bottom_line, top_line, True):
            return_value = Range(start_time, VelocityCalculator.time)

        if len(collision_times) == 0 or return_value is None:
            always_between_lines = is_between_lines and CollisionsUtilityFunctions.is_between_lines(line, bottom_line, top_line, True)
            # If the lines never collide and it is between the lines that means it was always between the lines otherwise it never was
            return_value = Range(0, 0) if not always_between_lines else Range(0, VelocityCalculator.time)

        return return_value

    def get_moving_collision_time(moving_object_path: ObjectPath, stationary_object):
        """ summary: Calls is_line_ellipse_collision() or is_line_rectangle_collision()
                     depending on if the stationary object is elliptical or rectangular; NOTE make sure to call only if
                     the objects from the previous cycle aren't touching otherwise it may not work properly

            params:
                moving_object_path: Path; the moving object's path
                stationary_object: GameObject; the object that isn't moving

            returns: boolean; if the moving object's path collides with the stationary object
        """

        collision_time = float('inf')
        for line in moving_object_path.get_lines():
            time = None
            if isinstance(stationary_object, Ellipse):
                time = CollisionsUtilityFunctions.get_line_ellipse_collision_time(line, stationary_object, moving_object_path)

            elif isinstance(stationary_object, LineSegment):
                time = CollisionsUtilityFunctions.get_line_collision_time(stationary_object, line, moving_object_path)

            # Assumes that if it isn't any of the above things it must be a rectangle
            else:
                time = CollisionsUtilityFunctions.get_line_rectangle_collision_time(stationary_object, line, moving_object_path)

            if time != -1 and time < collision_time:
                collision_time = time

        return collision_time if collision_time != float('inf') else -1

    def get_line_rectangle_collision_time(rectangle: GameObject, line: LineSegment, moving_object_path: ObjectPath):
        """returns: Point; the point at which the rectangle and line collide (None if they don't collide)"""

        rectangle_lines = [
            LineSegment(Point(rectangle.x_coordinate, rectangle.y_coordinate), Point(rectangle.x_coordinate, rectangle.bottom)),
            LineSegment(Point(rectangle.x_coordinate, rectangle.bottom), Point(rectangle.right_edge, rectangle.bottom)),
            LineSegment(Point(rectangle.right_edge, rectangle.bottom), Point(rectangle.right_edge, rectangle.y_coordinate)),
            LineSegment(Point(rectangle.right_edge, rectangle.y_coordinate), Point(rectangle.x_coordinate, rectangle.y_coordinate))
        ]

        collision_time = float('inf')
        for rectangle_line in rectangle_lines:
            time = CollisionsUtilityFunctions.get_line_collision_time(rectangle_line, line, moving_object_path)
            collision_time = time if time < collision_time and time != -1 else collision_time

        return collision_time if collision_time != float('inf') else -1

    def get_line_collision_time(static_line, moving_object_line, moving_object_path):
        """returns: double; the time of that the two lines collide"""

        return_value = -1
        collision_point = CollisionsUtilityFunctions.get_line_collision_point(static_line, moving_object_line)

        if collision_point is not None:
            distance_to_point = get_distance(moving_object_line.start_point, collision_point)
            time = CollisionsUtilityFunctions.get_time_to_point(distance_to_point, moving_object_path.get_total_distance())
            return_value = time

        return return_value

    def get_smallest_time(line: LineSegment, moving_object_path: ObjectPath, points):
        """returns: double; the smallest amount of time it would take for the line to go from it starts to a point"""

        smallest_time = float('inf')
        start_xy_point = moving_object_path.get_start_point()
        for point in points:
            xy_point = moving_object_path.get_xy_point(line, point)
            distance_to_point = get_distance(start_xy_point, xy_point)
            time = CollisionsUtilityFunctions.get_time_to_point(distance_to_point, moving_object_path.get_total_distance())
            smallest_time = time if time < smallest_time else smallest_time

        return smallest_time if smallest_time != float('inf') else -1

    def get_line_ellipse_collision_points(line, ellipse):
        # I'm using c in place of b since I have two b's one from the ellipse and the other from the line
        h, k, a, c = ellipse.get_equation_variables()

        m, b = line.slope, line.y_intercept

        # See documentation.md for where these numbers came from
        quadratic_a = pow(a, 2) * pow(m, 2) + pow(c, 2)
        quadratic_b = 2 * (pow(a, 2) * (b - k) * m - pow(c, 2) * h)
        quadratic_c = pow(a, 2) * pow(b - k, 2) + pow(c, 2) * pow(h, 2) - pow(a, 2) * pow(c, 2)

        x_coordinates = solve_quadratic(quadratic_a, quadratic_b, quadratic_c)

        # The difference between supposed_collision_points and collision_points is that collision_points takes into account
        # That it is a line segment while supposed_collision_points doesn't
        collision_points = []

        # TODO fix so there does not have to be a 2 return statements
        if x_coordinates is None:
            return []

        for x_coordinate in x_coordinates:
            for y_coordinate in ellipse.get_y_coordinate_min_and_max(x_coordinate):
                point = Point(x_coordinate, y_coordinate)

                if line.contains_point(point, CollisionsUtilityFunctions.point_deviation_allowed):
                    collision_points.append(point)

        return collision_points

    def get_line_ellipse_collision_time(line: LineSegment, ellipse: Ellipse, moving_object_path):
        """returns: Point; the point at which the line and the ellipse collide (None if they don't collide)"""

        collision_points = CollisionsUtilityFunctions.get_line_ellipse_collision_points(line, ellipse)
        return CollisionsUtilityFunctions.get_smallest_time(line, moving_object_path, collision_points)

    def get_time_to_point(distance_to_point, total_distance):
        """returns: double; the time it would take to reach that point and it returns -1 if the time it would take is
        greater than VelocityCalculator.time"""
        velocity = total_distance / VelocityCalculator.time

        time = distance_to_point / velocity
        # Multiplying by 1.1 for a little bit of a time buffer, so it doesn't discard an actual collision
        return time if time <= VelocityCalculator.time * 1.1 else -1

    def get_line_collision_point(line1, line2):
        """returns: Point; the point at which line1 and line2 collide (None if they don't collide)"""

        # If the lines are parallel they couldn't have collided
        if line1.slope == line2.slope:
            return None

        x_collision_point = (line2.y_intercept - line1.y_intercept) / (line1.slope - line2.slope)
        collision_point = None

        if line1.is_vertical or line2.is_vertical:
            vertical_line = line1 if line1.is_vertical else line2
            non_vertical_line = line2 if line1.is_vertical else line1
            x_collision_point = vertical_line.start_point.x_coordinate
            collision_point = Point(x_collision_point, non_vertical_line.get_y_coordinate(x_collision_point))

        else:
            collision_point = Point(x_collision_point, line1.get_y_coordinate(x_collision_point))

        # If one of the line segments doesn't contain that collision point then the lines couldn't have collided
        point_deviation_allowed = CollisionsUtilityFunctions.point_deviation_allowed
        if not line1.contains_point(collision_point, point_deviation_allowed) or not line2.contains_point(collision_point, point_deviation_allowed):
            collision_point = None

        return collision_point

    def is_line_collision(line1: LineSegment, line2: LineSegment):
        """returns: boolean; if the two lines have crossed"""

        return CollisionsUtilityFunctions.get_line_collision_point(line1, line2) is not None

    def get_path_line_collision_points(line: LineSegment, path: Path):
        """returns: Point; the x and y coordinate at which the line and path collide (None if they don't collide)"""

        return_value = []

        for path_line in path.get_lines():
            collision_point = CollisionsUtilityFunctions.get_line_collision_point(path_line, line)

            if collision_point is not None:
                return_value.append(collision_point)

        return return_value

    def get_bottommost_object(object1, object2):
        """ summary: finds the object whose y_coordinate is the biggest (top of the screen is 0)

              params:
                 object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                 object2: GameObject; one of the objects that is used to see if the two objects provided have collided

              returns: GameObject; the object that is on the bottom of the screen
         """
        return object1 if object1.y_coordinate > object2.y_coordinate else object2

    def get_topmost_object(object1, object2):
        """ summary: finds the object whose y_coordinate is the smallest (top of the screen is 0)

             params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

             returns: GameObject; the object that is on the top of the screen
        """

        return object1 if object1.y_coordinate < object2.y_coordinate else object2

    # TODO COLLISION FOR WHEN LINE ISN'T FROM A TO B; Maybe Combine w/ A to B Collision
    # TODO figure out a way to test this code specifically

    def get_big_path_collision_time(object1_paths, object2_paths):
        """ summary: finds the time that object1 and object2 collide using their paths

            params:
                object1_paths: List of Path; [object1 x path, object1 right edge path]- the path of object1


            returns: List of Collision; [object1 CollisionData, object2 CollisionData]"""

        x_path1, right_edge_path1, y_path1, bottom_path1 = object1_paths
        x_path2, right_edge_path2, y_path2, bottom_path2 = object2_paths

        x_ranges = []
        x_ranges += CollisionsUtilityFunctions.get_ranges_between(x_path1, x_path2, right_edge_path2)
        x_ranges += CollisionsUtilityFunctions.get_ranges_between(right_edge_path1, x_path2, right_edge_path2)
        x_ranges += CollisionsUtilityFunctions.get_ranges_between(x_path2, x_path1, right_edge_path1)
        x_ranges += CollisionsUtilityFunctions.get_ranges_between(right_edge_path2, x_path1, right_edge_path1)

        y_ranges = []
        y_ranges += CollisionsUtilityFunctions.get_ranges_between(y_path1, y_path2, bottom_path2)
        y_ranges += CollisionsUtilityFunctions.get_ranges_between(bottom_path1, y_path2, bottom_path2)
        y_ranges += CollisionsUtilityFunctions.get_ranges_between(y_path2, y_path1, bottom_path1)
        y_ranges += CollisionsUtilityFunctions.get_ranges_between(bottom_path2, y_path1, bottom_path1)

        x_ranges = CollisionsUtilityFunctions.filter_ranges(x_ranges)
        y_ranges = CollisionsUtilityFunctions.filter_ranges(y_ranges)
        return_value = float('inf')

        for x_range in x_ranges:
            for y_range in y_ranges:
                smaller_range = x_range if x_range.is_less_than(y_range) else y_range
                bigger_range = x_range if not x_range.is_less_than(y_range) else y_range
                # Meaning that the ranges share a similar point
                if smaller_range.end >= bigger_range.start and bigger_range.start < return_value:
                    time = bigger_range.start
                    return_value = time if time < return_value else return_value

        return return_value if return_value != float('inf') else -1

    def get_ranges_between(path: SimplePath, bottom_path: SimplePath, top_path: SimplePath):
        """returns: List of Range; the times that 'line' is between 'top_line' and 'bottom_line' NOTE: the lines must have
        time as their x coordinate and the coordinates (x, y, bottom, or right_edge) as the y coordinate"""

        collision_times = CollisionsUtilityFunctions.get_path_collision_times(path, bottom_path)
        collision_times += CollisionsUtilityFunctions.get_path_collision_times(path, top_path)

        collision_times.sort()
        collision_times = list(filter(lambda item: item > 0, collision_times))

        start_time = 0

        is_between_lines = CollisionsUtilityFunctions.is_between_lines(path.get_first_line(), bottom_path.get_first_line(), top_path.get_first_line(), False)

        return_value = []

        # TODO is this logic correct or inaccurate; what if it collides with the bottom line two times in a row?
        for collision_time in collision_times:
            if is_between_lines:
                return_value.append(Range(start_time, collision_time))

            is_between_lines = not is_between_lines
            start_time = collision_time

        if len(collision_times) == 0 or len(return_value) == 0:
            always_between_lines = is_between_lines and CollisionsUtilityFunctions.is_between_lines(path.get_last_line(), bottom_path.get_last_line(), top_path.get_last_line(), True)
            # If the lines never collide and it is between the lines that means it was always between the lines otherwise it never was
            return_value = [Range(0, 0)] if not always_between_lines else [Range(0, VelocityCalculator.time)]

        elif is_between_lines:
            # Since it ended in between the lines it must go from the previous collision time -> the end of the time of the paths
            return_value.append(Range(start_time, path.last_point.x_coordinate))

        return return_value

    def get_path_collision_times(path1, path2):

        collision_times = []

        for line1 in path1.get_lines():
            for line2 in path2.get_lines():

                collision_point = CollisionsUtilityFunctions.get_line_collision_point(line1, line2)

                # Meaning it is a collision
                if collision_point is not None:
                    collision_times.append(collision_point.x_coordinate)

        return collision_times

