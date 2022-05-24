import random
from copy import deepcopy

from base.engine_utility_classes import CollisionsUtilityFunctions
from base.equations import Point
from base.path import VelocityPath
from base.utility_classes import HistoryKeeper
from base.utility_functions import percentage_to_number, get_min_list_item
from base.engines import CollisionsFinder
from base.velocity_calculator import VelocityCalculator
from games.pong.pong_types.pong_type import PongType
from games.pong.pong_types.normal_pong import NormalPong
from base.important_variables import *
from base.drawable_objects import Ellipse
from base.colors import *
from base.events import TimedEvent


class PortalOpening(Ellipse):
    """An opening that allows objects to teleport through it"""

    attributes = ["x_coordinate", "y_coordinate"]
    ball_exiting_direction_is_right = None
    is_enabled = True

    def __init__(self, percent_right, percent_down, percent_length, percent_height, ball_exiting_direction_is_right):
        """ summary: initializes the object

            params:
                percent_right: int; the percent it is to right (percentage of screen_length)
                percent_down: int; the percent it is down (percentage of screen_height)
                percent_length: int; the length (percentage of screen_length)
                percent_height: int; the height (percentage of screen_height)
                ball_exiting_direction_is_right: boolean; the ball exits the portal going right

            returns: None
        """

        x = percentage_to_number(percent_right, screen_length)
        y = percentage_to_number(percent_down, screen_height)
        length = percentage_to_number(percent_length, screen_length)
        height = percentage_to_number(percent_height, screen_height)
        self.ball_exiting_direction_is_right = ball_exiting_direction_is_right
        super().__init__(x, y, length, height, green)

    def disable(self, color):
        """ summary: disables the portal opening
            params: None
            returns: None
        """

        self.color = color
        self.is_enabled = False

    def enable(self, color):
        """ summary: enables the portal opening
            params: None
            returns: None
        """

        self.color = color
        self.is_enabled = True


class Portal:
    """Composed of two portal openings that allows objects to teleport through them"""

    portal_opening1: PortalOpening = None
    portal_opening2: PortalOpening = None
    is_enabled = True
    enabled_color = None
    can_be_enabled_event: TimedEvent = None

    def __init__(self, portal_opening1, portal_opening2, color):
        """ summary: initializes the object

            params:
                portal_opening1: PortalOpening; the first portal opening of the portal
                portal_opening2: PortalOpening; the second portal opening of the portal
                color: tuple; the (Red, Green, Blue) values of the portal

            returns: None
        """

        portal_opening1.name = "portal1 "+str(random.random())+str(id(self.portal_opening1))
        portal_opening2.name = "portal2 "+str(random.random())+str(id(self.portal_opening2))
        self.portal_opening1 = portal_opening1
        self.portal_opening2 = portal_opening2
        self.portal_opening2.color, self.portal_opening1.color = color, color
        self.enabled_color = color

        self.can_be_enabled_event = TimedEvent(2.5, False)

    def teleport(self, portal_end: PortalOpening, object):
        """ summary: teleports the ball to the end of the portal provided

            params:
                portal_end: PortalOpening; the end of the portal that the object will be teleported to
                object: GameObject; the object which will be teleported

            returns: None
        """

        object.x_coordinate = portal_end.x_midpoint
        object.y_coordinate = portal_end.y_midpoint

    def run(self, ball):
        """ summary: runs all the logic for teleporting the ball

            params:
                ball: Ball; the ball of the game

            returns: None
        """

        # Stores value of is_enabled, which other things in this function modify
        is_enabled = self.is_enabled

        portal_opening1_collision = CollisionsFinder.is_collision(ball, self.portal_opening1)

        portal_opening2_collision = CollisionsFinder.is_collision(ball, self.portal_opening2)

        is_portal_collision = portal_opening1_collision or portal_opening2_collision

        self.can_be_enabled_event.run(False, is_portal_collision)

        # If the ball was just teleported to it, it shouldn't be able to teleport again
        if portal_opening2_collision and is_enabled:
            self.teleport(self.portal_opening1, ball)


        if portal_opening1_collision and is_enabled:
            self.teleport(self.portal_opening2, ball)

        if is_portal_collision:
            self.disable()



    def render(self):
        """ summary: renders the portal
            params: None
            returns: None
        """

        self.portal_opening1.render()
        self.portal_opening2.render()

    def disable(self):
        """ summary: disables the portal
            params: None
            returns: None
        """

        self.portal_opening1.disable(light_gray)
        self.portal_opening2.disable(light_gray)
        self.is_enabled = False

    def enable(self):
        """ summary: enables the portal
            params: None
            returns: None
        """

        self.portal_opening1.enable(self.enabled_color)
        self.portal_opening2.enable(self.enabled_color)
        self.is_enabled = True


class PortalPong(PongType):
    """Pong where there are portals"""

    total_time = 0

    portal_length_percent = 15
    portal_height_percent = 15
    portals = [
        Portal(
            PortalOpening(10, 0, portal_length_percent,
                          portal_height_percent, False),
            PortalOpening(100 - portal_length_percent, 100 - portal_height_percent, portal_length_percent,
                          portal_height_percent, True), blue
        ),
        Portal(
            PortalOpening(100 - portal_length_percent, 10, portal_length_percent,
                          portal_height_percent, True),
            PortalOpening(10, 100 - portal_height_percent, portal_length_percent,
                          portal_height_percent, False), green
        )
    ]
    portal_openings = []
    portal_paths: [VelocityPath] = []
    data = ""
    has_added = False
    has_written = False
    test_number = 0
    s = ""

    def __init__(self, player1, player2, ball):
        """ summary: Initializes the PongType with the needed objects to run its methods

            params:
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """

        super().__init__(player1, player2, ball)
        
        self.normal_pong = NormalPong(player1, player2, ball)

        self.portal_openings = []

        for portal in self.portals:
            portal_opening1 = portal.portal_opening1
            portal_opening2 = portal.portal_opening2

            self.portal_openings.append(portal_opening1)
            self.portal_openings.append(portal_opening2)

            movement_velocity = VelocityCalculator.give_velocity(screen_length, 150)
            self.portal_paths.append(self.get_portal_opening_path(portal_opening1, portal_opening2, movement_velocity))
            self.portal_paths.append(self.get_portal_opening_path(portal_opening2, portal_opening1, movement_velocity))

    def get_portal_opening_path(self, portal_opening1, portal_opening2, movement_velocity):
        """ summary: creates a path for portal_opening1; from portal_opening1 -> portal_opening2 -> portal_opening1

            params:
                portal_opening1: PortalOpening; the portal opening which the path will be created for
                portal_opening2: PortalOpening; the portal opening which portal_opening1 will travel towards

            returns: VelocityPath; the path that portal_opening1 should take
        """

        path = VelocityPath(Point(portal_opening1.x_coordinate, portal_opening1.y_coordinate),
                            [Point(portal_opening2.x_coordinate, portal_opening2.y_coordinate),
                            Point(portal_opening1.x_coordinate, portal_opening1.y_coordinate)], movement_velocity)

        path.is_unending = True

        return path

    def run(self):
        """ summary: runs all the necessary things in order for this game mode to work
            params: None
            returns: None
        """

        self.total_time += VelocityCalculator.time

        self.normal_pong.ball_movement()
        self.normal_pong.run_player_movement()

        if CollisionsFinder.is_collision(self.ball, self.player1) or CollisionsFinder.is_collision(self.ball, self.player2):
            self.enable_portals()

        # Must come after logic of enabling portals otherwise the code above could have not detected a collision because
        # The ball has already moved (from the collision) by the time it has reached that code
        self.normal_pong.ball_collisions()

        for x in range(len(self.portals)):
            portal = self.portals[x]

            portal_opening1_collision = CollisionsFinder.is_collision(self.ball, portal.portal_opening1)
            portal_opening2_collision = CollisionsFinder.is_collision(self.ball, portal.portal_opening2)
            is_portal_collision = portal_opening1_collision or portal_opening2_collision

            po1 = portal.portal_opening1
            po2 = portal.portal_opening2

            portal_xy = f"po1 ({po1.x_coordinate}, {po1.y_coordinate})" if portal_opening1_collision else f"po2 ({po2.x_coordinate}, {po2.y_coordinate})"
            new_ball_xy = f"({po1.x_midpoint}, {po1.y_midpoint})" if portal_opening2_collision else f"({po2.x_midpoint}, {po2.y_midpoint})"

            portal.run(self.ball)

            portal_opening1 = portal.portal_opening1
            portal_opening2 = portal.portal_opening2

            # The portal paths list is twice as long as the portal list, so I have to multiply it by 2
            portal_opening1.x_coordinate, portal_opening1.y_coordinate = self.portal_paths[x * 2].get_coordinates()
            portal_opening2.x_coordinate, portal_opening2.y_coordinate = self.portal_paths[x * 2 + 1].get_coordinates()

        self.draw_game_objects()
        self.add_needed_objects()

    def enable_portals(self):
        """Enables all the portals"""

        for portal in self.portals:

            if portal.can_be_enabled_event.is_done():
                portal.enable()
                portal.can_be_enabled_event.reset()

    def reset(self):
        """ summary: resets all the necessary things (called after someone scores)
            params: None
            returns: None
        """

        self.normal_pong.reset()

    def draw_game_objects(self):
        """ summary: draws everything in this game mode
            params: None
            returns: None
        """

        for portal in self.portals:
            portal.render()
        super().draw_game_objects()
    
    def add_needed_objects(self):
        """ summary: adds all the objects to the HistoryKeeper
            params: None
            returns: None
        """

        super().add_needed_objects()
        for portal in self.portals:
            HistoryKeeper.add(portal.portal_opening1, portal.portal_opening1.name, False)
            HistoryKeeper.add(portal.portal_opening2, portal.portal_opening2.name, False)

    def get_ai_data(self, ai_x_coordinate):
        """returns: [ball_y_coordinate, ball_time_to_ai]"""
        enabled_portals = []

        for portal in self.portals:
            if portal.is_enabled:
                enabled_portals.append(portal)

        portal_paths = deepcopy(self.portal_paths)

        ball_x_coordinate = self.ball.x_coordinate
        ball_y_coordinate = self.ball.y_coordinate
        ball_is_moving_down = self.ball.is_moving_down
        total_time = 0

        while True:
            hit_a_portal = False
            collision_times = []
            portal_openings = []
            portal_opening_paths = []

            ball_path_data = self.get_ball_path_data(ball_y_coordinate, ball_x_coordinate, ai_x_coordinate,
                                                      ball_is_moving_down)
            ball_path = ball_path_data[0]
            times = ball_path_data[2]
            ball_paths = VelocityPath.get_paths_from_path(ball_path, times)

            self.add_to_lists(collision_times, ai_x_coordinate, enabled_portals, ball_paths,
                              ball_x_coordinate, portal_opening_paths, portal_paths, portal_openings)

            filtered_collision_times = list(filter(lambda item: item != -1, collision_times))

            index_of_min_time, collision_time = 0, 0

            if len(filtered_collision_times) == 0:
                collision_time = -1

            else:
                index_of_min_time = collision_times.index(get_min_list_item(filtered_collision_times))
                collision_time = collision_times[index_of_min_time]

            if collision_time != -1:
                path_of_portal = portal_opening_paths[index_of_min_time]
                portal_opening = portal_openings[index_of_min_time]
                # Have to divide by two because there are two portal openings (collision_times, etc.) to every portal
                portal = enabled_portals[index_of_min_time // 2]

                coordinates = self.get_ball_coordinates(ball_paths[0], path_of_portal, portal_opening, collision_time)
                new_ball_x_coordinate, new_ball_y_coordinate, ball_collision_x_coordinate = coordinates

                self._set_portal_path_times(collision_time, portal_paths)

                total_time += collision_time

                enabled_portals.remove(portal)
                ball_is_moving_down = self.ball_direction_is_down(ball_y_coordinate, ball_x_coordinate,
                                                                  ball_collision_x_coordinate, ball_is_moving_down)
                ball_x_coordinate, ball_y_coordinate = new_ball_x_coordinate, new_ball_y_coordinate
                hit_a_portal = True

            if not hit_a_portal:
                ball_path_data = self.get_ball_path_data(ball_y_coordinate, ball_x_coordinate, ai_x_coordinate,
                                                          ball_is_moving_down)

                ball_path, times = ball_path_data[0], ball_path_data[2]
                # The last time in this list is the total time
                total_time += times[len(times) - 1]

                ball_y_coordinate = ball_path.get_end_points()[0].y_coordinate

                break

        return [ball_y_coordinate, total_time]

    def _set_portal_path_times(self, time_to_collision, portal_paths):
        """Sets the portal paths time to the time for the collision; allows for accurate predictions of where the portals will be"""

        for portal_path in portal_paths:
            portal_path.set_time(portal_path.total_time + time_to_collision)

    def get_ball_coordinates(self, ball_x_path, path_of_portal: VelocityPath, portal_opening, collision_time):
        """ summary: finds the necessary ball coordinates for figuring out the time and y coordinate of the ball for the ai

            params:
                ball_x_path: SimplePath; the ball's x coordinate path in relation to time (time being x and x_coordinate being y)
                path_of_portal: VelocityPath; the path of the portal which the ball will teleport to
                collision_time: double; the time of the ball's collision with the portal
                portal_opening: PortalOpening; the portal which the ball will be teleported to

            returns: Double[3]; [new_ball_x_coordinate, new_ball_y_coordinate, ball_collision_x_coordinate]
        """

        portal_x_coordinate, portal_y_coordinate = path_of_portal._get_coordinates(collision_time + path_of_portal.total_time)
        # Have to add length / 2 and height / 2 because the ball teleports to the middle of the portal
        new_ball_x_coordinate = portal_x_coordinate + portal_opening.length / 2
        new_ball_y_coordinate = portal_y_coordinate + portal_opening.height / 2

        ball_collision_x_coordinate = ball_x_path.get_y_coordinate(collision_time)

        return [new_ball_x_coordinate, new_ball_y_coordinate, ball_collision_x_coordinate]

    def add_to_lists(self, collision_times, ai_x_coordinate, enabled_portals, ball_paths, ball_x_coordinate, portal_opening_paths, portal_paths, portal_openings):
        """Adds all the necessary data to the lists provided for figuring out where the ball is going to end up"""

        for portal in enabled_portals:
            total_time = (ai_x_coordinate - ball_x_coordinate) / self.ball.forwards_velocity
            portal_opening1 = portal.portal_opening1
            portal_opening2 = portal.portal_opening2

            index = self.portals.index(portal)

            # Portal paths list is twice as big because it is for the portal openings not just the portal
            portal_opening1_path: VelocityPath = portal_paths[index * 2]
            portal_opening2_path: VelocityPath = portal_paths[index * 2 + 1]

            portal_opening1_paths = portal_opening1_path.get_paths(portal_opening1.length, portal_opening1.height,
                                                                   total_time)
            portal_opening2_paths = portal_opening2_path.get_paths(portal_opening2.length, portal_opening2.height,
                                                                   total_time)

            collision_times.append(CollisionsUtilityFunctions.get_big_path_collision_time(portal_opening1_paths, ball_paths))
            collision_times.append(CollisionsUtilityFunctions.get_big_path_collision_time(portal_opening2_paths, ball_paths))

            # The order which the portal openings and portal paths are added must be the inverse of the
            # collision_times because they are where the portal will be teleported if it collided with a portal_opening
            portal_openings += [portal_opening2, portal_opening1]
            portal_opening_paths += [portal_opening2_path, portal_opening1_path]