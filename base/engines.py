from copy import deepcopy

from base.drawable_objects import GameObject, Ellipse
from base.engine_utility_classes import CollisionsUtilityFunctions, CollisionData
from base.equations import LineSegment
from base.path import Path, ObjectPath
from base.utility_classes import HistoryKeeper
from base.utility_functions import rounded

class CollisionsFinder:
    """Gives a series of methods to find if two (or more objects) have collided"""

    objects_to_data = {}

    # def update_data(object1, object2):

    def is_collision(object1, object2, last_time=None):
        CollisionsFinder.update_data(object1, object2, last_time)
        return CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}").is_collision
        # return CollisionsFinder.is_simple_collision(object1, object2)

    def is_moving_collision(object1, object2):
        CollisionsFinder.update_data(object1, object2)
        return CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}").is_moving_collision

    # VERY IMPORTANT NOTE: is moving left and right collisions count it if the object was not outside of the other last cycle
    # Meaning that if the object were to come down onto the end of the other object it would count; whereas left and right
    # Collisions it has to be on the outside last cycle in order for it to count
    def is_left_collision(object1, object2, is_collision=None, time=None):
        """returns: boolean; if object1 has collided with object2's left edge (movement does not matter)"""
        last_time = time if time is not None else HistoryKeeper.last_time
        prev_object1 = HistoryKeeper.get_last_from_time(object1.name, last_time)
        prev_object2 = HistoryKeeper.get_last_from_time(object2.name, last_time)

        if prev_object1 is None or prev_object2 is None:
            return False

        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_collision(object1, object2)

        object1_has_moved_into_object2 = prev_object1.right_edge < prev_object2.x_coordinate and object1.right_edge > object2.x_coordinate
        is_moving_left_collision = is_collision and object1_has_moved_into_object2

        objects_are_touching = object1.right_edge == object2.x_coordinate and CollisionsFinder.is_height_collision(object1, object2)
        return is_moving_left_collision or objects_are_touching

    def is_right_collision(object1, object2, is_collision=None, time=None):
        """returns: boolean; if object1 has collided with object2's right_edge (movement does not matter)"""

        last_time = time if time is not None else HistoryKeeper.last_time
        prev_object1 = HistoryKeeper.get_last_from_time(object1.name, last_time)
        prev_object2 = HistoryKeeper.get_last_from_time(object2.name, last_time)

        if prev_object1 is None or prev_object2 is None:
            return False

        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_collision(object1, object2)
        object1_has_moved_into_object2 = (prev_object1.x_coordinate > prev_object2.right_edge and object1.x_coordinate < object2.right_edge)
        is_moving_right_collision = is_collision and object1_has_moved_into_object2

        objects_are_touching = object1.x_coordinate == object2.right_edge and CollisionsFinder.is_height_collision(object1, object2)
        return is_moving_right_collision or objects_are_touching

    def is_moving_right_collision(object1, object2):
        """returns: boolean; if object1 has collided with object2's right_edge because one of the objects has moved"""
        CollisionsFinder.update_data(object1, object2)
        collision_data: CollisionData = CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}")
        return collision_data.is_moving_collision and collision_data.is_moving_right_collision

    def is_moving_left_collision(object1, object2):
        """ returns: boolean; if object1 has hit object2's x_coordinate because one of the objects has moved"""

        CollisionsFinder.update_data(object1, object2)
        collision_data: CollisionData = CollisionsFinder.get_collision_data(object1, object2)
        return collision_data.is_moving_collision and collision_data.is_moving_left_collision

    def get_collision_data(object1, object2) -> CollisionData:
        """returns: CollisionData; the data for the collision for 'object1' and 'object2'"""
        return CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}")

    def get_objects_xy(object1, object2):
        """returns: List of Point; [object1's xy, object2's xy]"""
        CollisionsFinder.update_data(object1, object2)
        return [CollisionsFinder.get_collision_data(object1, object2).object_xy,
                CollisionsFinder.get_collision_data(object2, object1).object_xy]

    def make_dimensions_match(prev_object, current_object):
        """Makes the height and length of the objects match; changes prev_object to match current_object"""

        height_difference = current_object.height - prev_object.height
        length_difference = current_object.length - prev_object.length

        prev_object.height = current_object.height
        prev_object.length = current_object.length
        prev_object.x_coordinate -= length_difference
        prev_object.y_coordinate -= height_difference

    def update_data(object1: GameObject, object2: GameObject, last_time=None):
        """ summary: uses get_x_coordinates() and get_y_coordinates_from_x_coordinate() (methods from GameObject)
            to check if the objects share a point(s) (x_coordinate, y_coordinate)

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the two objects provided have collided
        """

        time = HistoryKeeper.last_time if last_time is None else last_time
        prev_object1 = HistoryKeeper.get_last_from_time(object1.name, time)
        prev_object2 = HistoryKeeper.get_last_from_time(object2.name, time)

        # Prevents None Type Error and saving these coordinates because they have to be modified if the length or height of the object has changed
        prev_object1_dimensions = [prev_object1.x_coordinate, prev_object1.y_coordinate, prev_object1.length, prev_object1.height] if prev_object1 is not None else [0,0,0,0]
        prev_object2_dimensions = [prev_object2.x_coordinate, prev_object2.y_coordinate, prev_object2.length, prev_object2.height] if prev_object2 is not None else [0,0,0,0]

        object1_has_moved, object2_has_moved = False, False

        if prev_object1 is None or prev_object2 is None:
            # There couldn't have been a collision since both either object1 or object2 didn't exist before this, so
            # objects_to_data should reflect that there is no collision
            CollisionsFinder.objects_to_data[f"{id(object2)} {id(object1)}"] = CollisionData(False, False, False, (0, 0), (0, 0))
            CollisionsFinder.objects_to_data[f"{id(object1)} {id(object2)}"] = CollisionData(False, False, False, (0, 0), (0, 0))
            return

        else:
            CollisionsFinder.make_dimensions_match(prev_object1, object1)
            CollisionsFinder.make_dimensions_match(prev_object2, object2)
            object1_has_moved = CollisionsFinder.object_has_moved(prev_object1, object1)
            object2_has_moved = CollisionsFinder.object_has_moved(prev_object2, object2)
        # if CollisionsFinder.objects_to_data.__contains__(f"{id(object1)} {id(object2)}"):
        #     return

        object1_path = ObjectPath(prev_object1, object1)
        object2_path = ObjectPath(prev_object2, object2)
        collision_time = -1
        is_moving_collision = False

        if object2_has_moved and object1_has_moved:
            # 4 cases because there are two paths for the objects - 2^2 possible combinations
            collision_time = CollisionsUtilityFunctions.get_path_collision_time(object1_path, object2_path)
            # If the time is functionally zero it can be discounted
            # if is_within_range(0, collision_time, pow(10, -6)):
            #     collision_time = -1
            is_moving_collision = collision_time != -1

        elif object2_has_moved or object1_has_moved:
            stationary_object = object1 if not object1_has_moved else object2
            moving_object_path = object1_path if object1_has_moved else object2_path
            # 2 cases: one for the x coordinate path and the other for the right edge path
            collision_time = CollisionsUtilityFunctions.get_moving_collision_time(moving_object_path, stationary_object)

            # If they started out touching then it was not a moving collision; they were already collided beforehand
            if CollisionsFinder.objects_are_touching(prev_object1, prev_object2):
                is_moving_collision = False
                collision_time = -1

        if CollisionsFinder.objects_are_touching(object1, object2):
            # The last case where neither object has moved and is checking if the objects are touching each other
            collision_time = 0

        CollisionsFinder.objects_to_data[f"{id(object1)} {id(object2)}"] = CollisionsUtilityFunctions.get_collision_data(object1, object2, prev_object1, prev_object2, collision_time, is_moving_collision)
        CollisionsFinder.objects_to_data[f"{id(object2)} {id(object1)}"] = CollisionsUtilityFunctions.get_collision_data(object2, object1, prev_object2, prev_object1, collision_time, is_moving_collision)

        prev_object1.x_coordinate, prev_object1.y_coordinate, prev_object1.length, prev_object1.height = prev_object1_dimensions
        prev_object2.x_coordinate, prev_object2.y_coordinate, prev_object2.length, prev_object2.height = prev_object2_dimensions

    def objects_are_touching(object1, object2):
        """returns: booolean; if the objects are touching"""

        objects_were_touching_horizontally = (rounded(object1.x_coordinate, 7) == rounded(object2.right_edge, 7) or
                                              rounded(object2.x_coordinate, 7) == rounded(object1.right_edge, 7)) and CollisionsFinder.is_height_collision(object1, object2)
        objects_were_touching_vertically = (rounded(object1.y_coordinate, 7) == rounded(object2.bottom, 7) or
                                            object2.y_coordinate == rounded(object1.bottom, 7)) and CollisionsFinder.is_length_collision(object1, object2)

        return objects_were_touching_horizontally or objects_were_touching_vertically

    def is_height_collision(object1, object2):
        """ summary: finds out if the object's y_coordinates have collided

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if one of the object's y coordinates is within the other's y coordinates
        """

        return (object1.bottom >= object2.y_coordinate and
                object1.y_coordinate <= object2.bottom)

    def is_length_collision(object1, object2):
        """ summary: finds out if the object's x coordinates have collided

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if one of the object's x coordinates is within the other's x coordinates
        """

        return (object1.x_coordinate <= object2.right_edge and
                object1.right_edge >= object2.x_coordinate)

    def is_simple_collision(object1, object2):
        """returns: boolean; if it is a simple collision --> does not check what happened in the past (just this frame)"""

        return CollisionsFinder.is_height_collision(object1, object2) and CollisionsFinder.is_length_collision(object1, object2)

    def is_a_bottom_collision(object1, object2, is_collision=None, time=None):
        """returns: boolean; if either object1 or object2 collided with the other one's bottom"""

        return CollisionsFinder.is_bottom_collision(object1, object2, is_collision, time) or CollisionsFinder.is_bottom_collision(object2, object1, is_collision, time)

    def is_a_top_collision(object1, object2, is_collision=None, time=None):
        """returns: boolean; if either object1 or object2 collided with the other one's top"""

        return CollisionsFinder.is_top_collision(object1, object2, is_collision, time) or CollisionsFinder.is_top_collision(object2, object1, is_collision, time)

    def is_bottom_collision(object1, object2, is_collision=None, time=None):
        """ summary: finds out if the object's collided from the bottom
            
            params: 
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided
            
            returns: boolean; if the object's collided from the bottom
        """
        last_time = time if time is not None else HistoryKeeper.last_time
        prev_object1 = HistoryKeeper.get_last_from_time(object1.name, last_time)
        prev_object2 = HistoryKeeper.get_last_from_time(object2.name, last_time)

        if prev_object1 is None or prev_object2 is None:
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        objects_are_touching = object1.y_coordinate == object2.bottom and CollisionsFinder.is_length_collision(object1, object2)
        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_collision(object1, object2)


        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.y_coordinate > prev_object2.bottom and
                object1.y_coordinate < object2.bottom) or objects_are_touching

    def is_top_collision(object1, object2, is_collision=None, time=None):
        """ summary: finds out if the object's collided from the bottom

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object's collided from the bottom
        """

        last_time = time if time is not None else HistoryKeeper.last_time
        prev_object1 = HistoryKeeper.get_last_from_time(object1.name, last_time)
        prev_object2 = HistoryKeeper.get_last_from_time(object2.name, last_time)

        if prev_object1 is None or prev_object2 is None:
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        objects_are_touching = object1.bottom == object2.y_coordinate and CollisionsFinder.is_length_collision(object1, object2)
        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_collision(object1, object2)

        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.bottom < prev_object2.y_coordinate
                and object1.bottom > object2.y_coordinate) or objects_are_touching

    def get_path_line_collision(path, line):
        """returns: Point; the point with the smallest x coordinate in CollisionUtilityFunctions.get_path_line_collision_points()"""

        smallest_point = None
        smallest_x_coordinate = float("inf")
        for point in CollisionsUtilityFunctions.get_path_line_collision_points(line, path):
            if point.x_coordinate < smallest_x_coordinate:
                smallest_point = point
                smallest_x_coordinate = point.x_coordinate
        return smallest_point

    def is_line_ellipse_collision(line, ellipse):
        return len(CollisionsUtilityFunctions.get_line_ellipse_collision_points(line, ellipse)) != 0

    def object_has_moved(prev_obect, object):
        """returns: boolean; if the object has moved"""

        # Have to round the numbers otherwise there is a weird python rounding thing with floats
        return (rounded(prev_obect.x_coordinate - object.x_coordinate, 4) != 0 or
                rounded(prev_obect.y_coordinate - object.y_coordinate, 4) != 0)