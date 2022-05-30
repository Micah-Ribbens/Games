from copy import deepcopy

import pygame

from base.engine_utility_classes import CollisionsUtilityFunctions
from base.engines import CollisionsFinder
from base.equations import Point, LineSegment
from base.events import Event
from base.game_movement import GameMovement
from base.important_variables import screen_height, screen_length
from base.path import VelocityPath, Path, SimplePath
from games.pong.base_pong.players import Player, AI
from base.utility_classes import HistoryKeeper, StateChange
from base.utility_functions import get_rightmost_object, get_displacement, min_value, max_value
from base.velocity_calculator import VelocityCalculator
from games.pong.pong_types.normal_pong import NormalPong
from base.utility_functions import get_min_list_item, get_index_of_min_item, get_converted_list


# TODO fix code so you don't have to assume player2 is the ai
# TODO write the code so it takes into account both vertical and horizontal time
class OmnidirectionalPong(NormalPong):
    """Pong where the player can move 4 directions"""''
    # States for the AI
    should_stop = False

    class States:
        GOING_TOWARDS_GOAL = "GOING_TOWARDS_GOAL"
        INTERCEPTING_BALL = "INTERCEPTING_BALL"
        CENTERING = "CENTERING"
        BACKING_UP = "BACKING_UP"
        INTERCEPTING_PLAYER = "INTERCEPTING_PLAYER"
        WAITING = "WAITING"
        WAITING_FOR_SPAWN = "WAITING_FOR_SPAWN"

    current_state = States.INTERCEPTING_BALL
    next_state = States.INTERCEPTING_BALL

    ball_sandwiched_event = Event()
    ball_is_spawned = False
    a_player_has_scored = False

    # Stores the value of the ball at the start of the cycle; the ball gets modified in the code making this necesary
    last_ball = None
    debug = False
    ball_data = None
    ball_y_path = None
    ball_x_path = None
    ball_right_edge_path = None
    ball_bottom_path = None

    player_who_hit_ball_key = "player who hit ball"
    player_path = None
    is_top_or_bottom_collision = False

    def __init__(self, player1, player2, ball):
        """ summary: Initializes the PongType with the needed objects to run its methods

            params:
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """

        super().__init__(player1, player2, ball)
        self.last_ball = self.ball
        self.player1.can_move_left, self.player2.can_move_left = False, False
        self.player1.can_move_right, self.player2.can_move_right = False, False

    def set_player_coordinates(self):
        """Sets the players coordinates and their ability to move after a collision"""

        CollisionsFinder.is_moving_collision(self.player1, self.player2)
        player1_xy, player2_xy = CollisionsFinder.get_objects_xy(self.player1, self.player2)
        is_top_or_bottom_collision = self.is_top_or_bottom_collision
        self.player1.x_coordinate, self.player1.y_coordinate = player1_xy.x_coordinate, player1_xy.y_coordinate
        self.player2.x_coordinate, self.player2.y_coordinate = player2_xy.x_coordinate, player2_xy.y_coordinate

        # Horizontal Movement
        if not is_top_or_bottom_collision:
            self.get_leftmost_player().can_move_right = False
            self.get_rightmost_player().can_move_left = False

        if self.get_leftmost_player() == self.player2 and not is_top_or_bottom_collision:
            self.player2.x_coordinate = self.player1.x_coordinate - self.player2.length

        elif not is_top_or_bottom_collision:
            self.player2.x_coordinate = self.player1.right_edge

        # Vertical Movement
        top_player = CollisionsUtilityFunctions.get_topmost_object(self.player1, self.player2)
        bottom_player = CollisionsUtilityFunctions.get_bottommost_object(self.player1, self.player2)

        if is_top_or_bottom_collision:
            bottom_player.can_move_up = False
            top_player.can_move_down = False

            # Shouldn't have to do this, but a really weird float not being precise error is occuring
            bottom_player.y_coordinate = top_player.bottom
            top_player.y_coordinate = bottom_player.y_coordinate - top_player.height

    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """

        # ORDER MATTERS! This must go first
        if self.ball.can_move:
            self.ball_movement()

        self.last_ball = self.ball
        GameMovement.player_horizontal_movement(self.player1, self.player1.velocity, pygame.K_a, pygame.K_d)
        self.player1.movement()

        if self.is_single_player:
            self.player2.action = self.run_ai
            self.player2.run()

        else:
            self.player2.movement()
            GameMovement.player_horizontal_movement(self.player2, self.player2.velocity, pygame.K_LEFT, pygame.K_RIGHT)

        self.set_is_top_or_bottom_collision()
        self.set_player_horizontal_movements(self.player2)
        self.set_player_horizontal_movements(self.player1)
        self.run_player_boundaries(self.player2)
        self.run_player_boundaries(self.player1)

        self.ball_sandwiched_event.run(self.ball_is_sandwiched())
        # Collisions
        self.ball_collisions(self.player1)
        self.ball_collisions(self.player2)
        self.paddle_collisions()
        self.run_ball_sandwiching()

    def set_is_top_or_bottom_collision(self):
        """Stores whether the players have collided with each other's top or bottom in a variable, which can be accessed by the code"""

        is_moving_top_or_bottom_collision = (CollisionsFinder.is_a_top_collision(self.player1, self.player2)
                                             or CollisionsFinder.is_a_bottom_collision(self.player1, self.player2))

        # Prevents a weird rounding error by casting them to integers
        players_top_and_bottoms_are_touching = (int(self.player1.bottom) == int(self.player2.y_coordinate) or
                                                int(self.player2.bottom) == int(self.player1.y_coordinate))

        self.is_top_or_bottom_collision = is_moving_top_or_bottom_collision or players_top_and_bottoms_are_touching

    def paddle_collisions(self):
        """ summary: runs all the collisions between paddles
            params: None
            returns: None
        """

        if CollisionsFinder.is_moving_collision(self.player1, self.player2):
            self.set_player_coordinates()
        self.run_player_boundaries(self.player1)
        self.run_player_boundaries(self.player2)

    def run_ball_sandwiching(self):
        """ summary: runs all the logic necessary for the ball to stop when it's "sandwiched" between two players
            params: None
            returns: None
        """

        if self.ball_is_sandwiched():
            self.ball.x_coordinate = self.get_leftmost_player().right_edge
            self.ball.can_move = False

        else:
            self.ball.can_move = True

        if self.ball_is_sandwiched() and not self.ball_sandwiched_event.happened_last_cycle():
            rightmost_player = self.get_rightmost_player()
            leftmost_player = self.get_leftmost_player()

            rightmost_player.x_coordinate = self.ball.right_edge
            leftmost_player.x_coordinate = self.ball.x_coordinate - leftmost_player.length
            rightmost_player.can_move_left = False
            leftmost_player.can_move_right = False

    def ball_collisions(self, player):
        """ summary: runs the collisions between the ball and that player

            params:
                player: Player; the player that will have its collisions between it and the ball run

            returns: None
        """
        if CollisionsFinder.is_moving_collision(self.last_ball, player):
            HistoryKeeper.add(player, self.player_who_hit_ball_key, True)
            velocity_reduction = .8
            player.velocity = player.base_velocity * velocity_reduction

        else:
            player.velocity = player.base_velocity

        if CollisionsFinder.is_moving_right_collision(self.last_ball, player) and not self.ball_is_sandwiched():
            self.ball.x_coordinate = player.right_edge
            self.ball.is_moving_right = True
            HistoryKeeper.add(player, self.player_who_hit_ball_key, True)

        elif CollisionsFinder.is_moving_left_collision(self.last_ball, player) and not self.ball_is_sandwiched():
            CollisionsFinder.is_moving_left_collision(self.last_ball, player)
            self.ball.x_coordinate = player.x_coordinate - self.ball.length
            self.ball.is_moving_right = False
            HistoryKeeper.add(player, self.player_who_hit_ball_key, True)

        self.ball_screen_boundary_collisions(self.ball)

    def horizontal_player_movements(self, player, left_key, right_key):
        """Runs the horizontal movement of the player"""

        controls = pygame.key.get_pressed()



    def set_player_horizontal_movements(self, player):
        """Sets the directions that the player can move"""

        is_collision = CollisionsFinder.is_collision(self.player1, self.player2) or self.ball_is_sandwiched()
        within_screen_right = player.right_edge < screen_length
        within_screen_left = player.x_coordinate > 0

        if not is_collision and within_screen_right:
            player.can_move_right = True

        if not is_collision and within_screen_left:
            player.can_move_left = True

    def run_player_boundaries(self, player):
        """ summary: sets the players can move left and right based on if the player is within the screens bounds

            params:
                player: Player; the player that the boundaries will be checked for

            returns: None
        """
        if player.right_edge >= screen_length:
            player.x_coordinate = screen_length - player.length
            player.can_move_right = False

        if player.x_coordinate <= 0:
            player.x_coordinate = 0
            player.can_move_left = False

        if player.y_coordinate <= 0:
            player.can_move_up = False
            player.y_coordinate = 0

        if player.bottom >= screen_height:
            player.can_move_down = False
            player.y_coordinate = screen_height - player.height

        within_screen_bottom = player.bottom < screen_height
        within_screen_top = player.y_coordinate > 0
        other_player = self.player1 if player == self.player2 else self.player2

        player_is_on_top = CollisionsUtilityFunctions.get_topmost_object(player, other_player) == player

        # If the players have collided with one another's top or bottom they should not be able to keep moving that direction
        if within_screen_top and not (self.is_top_or_bottom_collision and not player_is_on_top):
            player.can_move_up = True

        if within_screen_bottom and not (self.is_top_or_bottom_collision and player_is_on_top):
            player.can_move_down = True

    def ball_is_sandwiched(self):
        """ summary: finds out if the ball is a within a certain distance between the two players and is within their height (sandwiched)
            params: None
            returns: boolean; if the ball is sandwiched
        """
        leftmost_player = self.get_leftmost_player()
        rightmost_player = self.get_rightmost_player()

        distance_between_players = rightmost_player.x_coordinate - leftmost_player.right_edge

        distance_needed = self.ball.length

        ball_is_between_players = (self.last_ball.x_coordinate >= leftmost_player.x_coordinate
                                           and self.last_ball.right_edge <= rightmost_player.right_edge)

        return distance_between_players <= distance_needed and self.ball_is_between_players() and ball_is_between_players

    def ball_is_between_players(self):
        """ summary: finds out if the players are at the same height and the ball's y coordinates are between the players
            params: None
            returns: boolean; the ball is between the players
        """

        leftmost_player = self.get_leftmost_player()
        rightmost_player = self.get_rightmost_player()

        players_are_at_same_height = CollisionsFinder.is_height_collision(leftmost_player, rightmost_player)
        ball_y_coordinate_is_between_players = (CollisionsFinder.is_height_collision(self.last_ball, rightmost_player)
                                                and CollisionsFinder.is_height_collision(self.last_ball, leftmost_player))

        return players_are_at_same_height and ball_y_coordinate_is_between_players

    def get_leftmost_player(self):
        """ summary: finds the player that is the most left on the screen and returns it
            params: None
            returns: Player; the leftmost player
        """
        return self.player1 if self.player1.x_coordinate < self.player2.x_coordinate else self.player2

    def get_rightmost_player(self):
        """ summary: finds the player that is the most right on the screen and returns it
            params: None
            returns: Player; the rightmost player
        """
        return self.player1 if self.player1.x_coordinate > self.player2.x_coordinate else self.player2

    def reset(self):
        """Resets everything necessary after someone scored"""
        super().reset()
        self.ball_is_spawned = True
        self.a_player_has_scored = True

    # AI CODE
    def run_ai(self):
        # So when it is first initialized there is a player path
        if self.next_state != self.current_state or self.player_path is None:
            self.run_state_changes()

        # BACKING_UP
        self.run_state_change(self.States.BACKING_UP, [
            StateChange(self.is_done_backing_up(), self.States.WAITING)])
        # INTERCEPTING_PLAYER
        self.run_state_change(self.States.INTERCEPTING_PLAYER, [
            StateChange(not self.can_intercept_object(self.player1.velocity, self.player1), self.States.CENTERING),
            StateChange(not CollisionsFinder.is_collision(self.player1, self.last_ball), self.States.INTERCEPTING_BALL)])
        # CENTERING
        self.run_state_change(self.States.CENTERING, [
            StateChange(self.ball_is_spawned, self.States.INTERCEPTING_BALL)])
        # INTERCEPTING_BALL
        self.run_state_change(self.States.INTERCEPTING_BALL, [
            StateChange(CollisionsFinder.is_moving_left_collision(self.player2, self.last_ball), self.States.GOING_TOWARDS_GOAL),
            StateChange(not self.can_intercept_object(self.ball.forwards_velocity, self.last_ball), self.States.CENTERING),
            StateChange(CollisionsFinder.is_collision(self.player1, self.last_ball), self.States.INTERCEPTING_PLAYER)
        ])
        # WAITING
        prev_player = HistoryKeeper.get_last(self.player1.name)
        opponent_has_moved = prev_player is not None and prev_player.x_coordinate != self.player1.x_coordinate
        opponent_is_touching_ball = CollisionsFinder.is_collision(self.player1, self.last_ball)
        self.run_state_change(self.States.WAITING, [
            StateChange(opponent_has_moved and opponent_is_touching_ball and self.ball.x_coordinate >= self.player2.right_edge, self.States.INTERCEPTING_PLAYER),
            StateChange(self.ball.is_moving_right and self.ball.x_coordinate >= self.player2.right_edge, self.States.INTERCEPTING_BALL)])
        # State Changes no matter what State
        prev = self.next_state
        self.next_state = self.States.BACKING_UP if self.ball_is_sandwiched() else self.next_state
        self.next_state = self.States.INTERCEPTING_BALL if self.a_player_has_scored and self.ball_is_spawned else self.next_state

        if prev != self.next_state:
            print("CALLED THROUGH TRANSITION")

        if self.player_path is not None:
            self.player2.x_coordinate, self.player2.y_coordinate = self.player_path.get_coordinates()

        # Done using this variable, so it should be False again
        self.a_player_has_scored = False

    def can_intercept_object(self, intercepted_object_velocity, intercepted_object):
        """returns: boolean; if the AI can intercept that object (assumes the object is going rightwards); only takes into account x coordinate"""
        return_value = True

        distance_needed = intercepted_object.right_edge - self.player2.x_coordinate

        velocity_difference = self.player2.velocity - intercepted_object_velocity

        if velocity_difference <= 0 and distance_needed > 0:
            return_value = False

        else:
            # The max amount of time the AI has to travel the distance
            max_time = (screen_length - intercepted_object.right_edge) / intercepted_object_velocity

            return_value = (distance_needed / velocity_difference) <= max_time

        return return_value

    def is_done_backing_up(self):
        """returns: boolean; if the AI is done backing away from the ball"""
        return_value = False

        # Assumes the backing up path is one singular line
        start_x_coordinate: Point = self.player_path.x_coordinate_lines[0].start_point.y_coordinate
        end_x_coordinate: Point = self.player_path.x_coordinate_lines[0].end_point.y_coordinate

        path_is_leftwards = start_x_coordinate > end_x_coordinate

        if path_is_leftwards and self.player2.x_coordinate <= end_x_coordinate:
            return_value = True

        if not path_is_leftwards and self.player2.x_coordinate >= end_x_coordinate:
            return_value = True

        return return_value

    def run_state_change(self, needed_state, states_changes):
        """ summary: changes the attribute 'next_state' if one of the state change's condition is True

            params:
                needed_state: int; the state that the AI has to be in in order to change states
                state_changes: List of StateChange; the states that are allowed
        """

        for state_change in states_changes:
            if state_change.condition and self.current_state == needed_state:
                self.next_state = state_change.state

    def run_state_changes(self):
        """Runs all the code that should be done when the state changes"""
        self.update_ball_data()
        # GOING_TOWARDS_GOAL
        if self.next_state == self.States.GOING_TOWARDS_GOAL:
            self.go_to_goal()

        # INTERCEPTING_BALL
        if self.next_state == self.States.INTERCEPTING_BALL:
            self.intercept_object(self.ball.forwards_velocity, self.ball, self.ball.is_moving_right, self.player2)

        # INTERCEPTING_PLAYER
        if self.next_state == self.States.INTERCEPTING_PLAYER:
            # The ball is touching the player so it has to intercept the ball that is touching the player
            self.intercept_object(self.player2.forwards_velocity, self.ball, False, self.player2)

        # BACKING_UP
        if self.next_state == self.States.BACKING_UP:
            self.player_path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [], self.player2.velocity)
            self.player_path.add_point(Point(self.player2.x_coordinate + 50, self.player2.y_coordinate + 10))

        # CENTERING
        if self.next_state == self.States.CENTERING:
            self.player_path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [], self.player2.velocity)
            self.player_path.add_point(Point(screen_length / 2, screen_height / 2))

        self.current_state = self.next_state

    def get_important_times(self):
        """Finds and returns the important times for the players path; important is being defined by points where a major
        change happens. The major changes are transitioning into the bottom of the screen and transitioning out of the bottom of the screen"""

        important_times = []

        for line in self.ball_y_path.get_lines():
            # Or more accurately the player transitions into the bottom of the screen or out of the bottom of the screen
            time_at_bottom = line.get_x_coordinate(screen_height - self.player2.height)
            min_time = line.start_point.x_coordinate
            max_time = line.end_point.x_coordinate

            player_is_at_bottom = time_at_bottom > min_time and time_at_bottom < max_time

            if player_is_at_bottom and line.slope_is_positive():
                important_times.append(time_at_bottom)

            elif player_is_at_bottom:
                important_times.append(time_at_bottom)

            if not important_times.__contains__(max_time):
                important_times.append(max_time)

        return important_times

    def get_horizontal_time(self, intercepted_objects_velocity, ball, is_moving_rightwards, player2):
        """returns: double; the time it will take for player2 to reach the ball horizontally"""

        intercept_object_x_line = LineSegment.get_line_segment(ball, intercepted_objects_velocity, True, True)
        ai_x_line = LineSegment.get_line_segment(player2, player2.velocity, False, True)

        if CollisionsUtilityFunctions.get_line_collision_point(intercept_object_x_line, ai_x_line) is None:
            print("NOO HOR FAILED")

        return CollisionsUtilityFunctions.get_line_collision_point(intercept_object_x_line, ai_x_line).x_coordinate

    def get_times(self, intercepted_objects_velocity, ball, is_moving_rightwards, player2):
        """ summary: finds the times for player2 to go from above/below the ball to hitting the ball the right direction

            params:
                intercepted_objects_velocity: double; the velocity of the object that is going to be intercepted
                ball: Ball; the ball of the game
                is_moving_rightwards: whether or not the intercepted object is moving rightwrads
                player2: Player; the AI and it must be above/below the ball when calling this function (can't be a y coordinate collision with the ball)

            returns: List of double; [horizontal_time, vertical_time]"""

        horizontal_time = self.get_horizontal_time(intercepted_objects_velocity, ball, is_moving_rightwards, player2)

        vertical_time = self.get_vertical_time(ball, is_moving_rightwards, player2)

        return [horizontal_time, vertical_time]

    def get_vertical_time_points(self, ai):
        """returns: Point[]; [vertical_y_time_point, vertical_bottom_time_point] | The times points (time, y_coordinate)
        for intercepting the ball depending on whether it goes for under and over respectively"""

        # Two possible cases; the ai moves down to collide with the ball or up to collide the ball (the quicker one will be used)
        ai_y_line = LineSegment.get_line_segment(ai, ai.velocity, False, False)
        ai_bottom_line = LineSegment.get_line_segment(ai, ai.velocity, True, False)

        vertical_y_time_point = self.get_vertical_time_point(self.ball_y_path, ai_bottom_line, ai.height)
        vertical_bottom_time_point = self.get_vertical_time_point(self.ball_bottom_path, ai_y_line, ai.height)

        return [vertical_y_time_point, vertical_bottom_time_point]

    def get_vertical_time(self, ball, is_moving_rightwards, player2):
        vertical_y_time_point, vertical_bottom_time_point = self.get_vertical_time_points(player2)
        return_value = []

        # The player cannot be above the screen or below the screen when trying to hit the ball
        if vertical_y_time_point is not None and vertical_y_time_point.y_coordinate <= screen_height - player2.height:
            return_value.append(vertical_y_time_point.x_coordinate)

        if vertical_bottom_time_point is not None and vertical_bottom_time_point.y_coordinate <= player2.height:
            return_value.append(vertical_bottom_time_point.x_coordinate)

        return get_min_list_item(return_value)

    def intercept_object(self, intercepted_objects_velocity, ball, is_moving_rightwards, ai):
        """ summary: makes the AI's path intercept the other object using the parameters

            params:
                intercepted_objects_velocity: double; the velocity of the intercepted_object
                intercepted_object: GameObject; the object that will be intercepted

            returns: None
        """

        path_is_leftwards = get_rightmost_object(ball, ai) == ai

        if path_is_leftwards:
            self.move_into_object(ball, ai, intercepted_objects_velocity)

        else:
            horizontal_time, vertical_time = self.get_times(intercepted_objects_velocity, ball, is_moving_rightwards, ai)
            self.get_in_front_of_ball(min_value(horizontal_time, vertical_time), ball, is_moving_rightwards)

    def move_into_object(self, ball, ai, object_velocity):
        """Adds the points to the path so the AI will move into the ball"""

        horizontal_distance = abs(ai.x_coordinate - ball.right_edge)

        # Have to take into account the ball's movement direction because that will either add to the total_velocity
        # that will close the gap or make it smaller
        total_velocity = ai.forwards_velocity + object_velocity if ball.is_moving_right else ai.forwards_velocity - object_velocity
        horizontal_time = horizontal_distance / total_velocity

        # Two cases; the AI can either go up into the object or down into the object
        upwards_y_midpoint_path = LineSegment.get_line_segment_using_coordinates(ai.y_midpoint, ai.velocity, False)
        downwards_y_midpoint_path = LineSegment.get_line_segment_using_coordinates(ai.y_midpoint, ai.velocity, True)
        height_adjustment = ai.height / 2

        time_points = [self.get_vertical_time_point(self.ball_y_path, upwards_y_midpoint_path, height_adjustment, ai),
                       self.get_vertical_time_point(self.ball_y_path, downwards_y_midpoint_path, height_adjustment, ai)]

        time_points = list(filter(lambda item: item is not None, time_points))
        times = get_converted_list(time_points, "x_coordinate")

        vertical_time = get_min_list_item(times)

        # The time that comes later is the more important time because that is where the AI will have to go
        time = max_value(vertical_time, horizontal_time)
        buffer = 5

        ball_right_edge, ball_y_coordinate = self.ball_x_path.get_y_coordinate(time) + ball.length, self.ball_y_path.get_y_coordinate(time)

        # The AI should move more backwards to make sure the object will go into it if it has to go backwards otherwise
        # It should move more into the object to make sure it doesn't somehow miss it
        ball_right_edge += buffer if ball_right_edge >= ai.x_coordinate else -buffer

        ai.path.add_time_point(Point(ball_right_edge, ball_y_coordinate), time)

    def get_vertical_time_point(self, ball_path, ai_path, height_adjustment: float, ai: AI) -> Point:
        """ summary: finds the time (x coordinate) and the y_coordinate (y coordinate) where the ball path and ai path intersect

            params:
                ball_path: SimplePath; the path of the ball
                ai_path: LineSegment; the ai path that is being tested- could be the bottom_path, y_midpoint_path, etc.
                height_adjustment: Double; the number that has to be subtracted from the ai_path, so it is the y coordinate instead of bottom, y_midpoint, etc.
                ai: AI; the ai of the game

            returns: Point; the point where the ball_path and ai_path intersect
        """

        return_value = None

        for line in ball_path.get_lines():
            distance = abs(ai_path.get_y_coordinate(0) - line.start_point.y_coordinate)
            ball_velocity = self.ball.upwards_velocity if self.is_closing_gap(line, ai_path) else -self.ball.upwards_velocity

            ai_velocity = ai.velocity if self.is_closing_gap(ai_path, line) else -ai.velocity
            total_velocity = ball_velocity + ai_velocity

            # Have to add the current time at the start because (displacement / velocity) only gives the additional time
            time = (distance / total_velocity) + line.start_point.x_coordinate
            point = Point(time, line.get_y_coordinate(time))

            if line.contains_x_coordinate(time, .05) and ai_path.contains_x_coordinate(time, .05):
                point.y_coordinate -= height_adjustment
                return_value = point
                break

        return return_value

    def is_closing_gap(self, line, other_line):
        """returns: boolean; if 'line' is closing the y_coordinate gap between it and the 'other_line'"""

        return_value = None
        higher_line = line if line.start_point.y_coordinate > other_line.start_point.y_coordinate else other_line

        if higher_line == line:
            return_value = not line.slope_is_positive()

        else:
            return_value = line.slope_is_positive()

        return return_value


    def get_in_front_of_ball(self, time, ball, ai):
        """Adds points to the path, so the AI will move in front of the ball"""

        ball_coordinates = Point(self.ball_x_path.get_y_coordinate(time), self.ball_y_path.get_y_coordinate(time))

        buffer = 5
        valid_y_coordinates = self.get_valid_y_coordinates(ball_coordinates.y_coordinate, ai, buffer,
                                                           self.ball_y_path.is_moving_down(time))

        ai_x_coordinate = ball_coordinates.x_coordinate + ball.length + buffer
        index = self.get_best_y_coordinate_index(ai.y_coordinate, valid_y_coordinates)

        ai.path.add_time_point(Point(ai_x_coordinate, valid_y_coordinates[index][0]), time)

        intercept_y_coordinate = valid_y_coordinates[index][1]
        time_to_intercept_ball = self.get_time_to_intercept_ball(ai.y_coordinate, intercept_y_coordinate, ai, time)
        total_time = time_to_intercept_ball + time

        # Have to be in front of the ball's right edge in order to intercept it
        intercept_x_coordinate = ball.right_edge + (total_time * ball.forwards_velocity) + buffer

        ai.path.add_time_point(Point(intercept_x_coordinate, intercept_y_coordinate), total_time)

    def get_valid_y_coordinates(self, ball_y_coordinate, ai, buffer, ball_is_moving_down):
        """returns: Double[][2]; [ [y_coordinate, intercept_y_coordinate] ] the valid y coordinates that the ai could
        move to go under or over the ball and then up into the ball"""

        return_value = []
        ball_bottom = ball_y_coordinate + self.ball.height

        under_y_coordinate = ball_bottom + buffer
        over_y_coordinate = ball_y_coordinate - buffer - ai.height

        # The intercept y coordinate is the y coordinate that the ball will be at to intercept the ball at that location
        under_intercept_y_coordinate = under_y_coordinate - (ai.height / 2)
        over_intercept_y_coordinate = over_y_coordinate + (ai.height / 2)

        if under_y_coordinate <= screen_height - ai.height:
            return_value.append([under_y_coordinate, under_intercept_y_coordinate])

        if over_y_coordinate >= 0:
            return_value.append([over_y_coordinate, over_intercept_y_coordinate])

        return return_value

    def get_time_to_intercept_ball(self, ai_y_coordinate, new_y_coordinate, ai, current_time):
        """returns: Double; the time it will take for the ai to go from under or over the ball to intercepting it"""

        ai_path = SimplePath(Point(current_time, ai_y_coordinate))

        distance = abs(ai_y_coordinate - new_y_coordinate)
        time_to_new_y_coordinate = distance / ai.forwards_velocity

        ai_path.add_point(Point(current_time + time_to_new_y_coordinate, new_y_coordinate))

        # Have to minus current_time because I want to get the additional time
        return get_min_list_item(CollisionsUtilityFunctions.get_path_collision_times(ai_path, self.ball_y_path)) - current_time

    def get_best_y_coordinate_index(self, ai_y_coordinate, valid_y_coordinates):
        """returns: double; the y coordinate that requires the least amount of movement for the ai"""

        distances = []

        for valid_y_coordinate in valid_y_coordinates:
            # Since valid_y_coordinates is a Double[][], I am accessing the first item- the initial y coordinate before moving to intercept
            distances.append(abs(ai_y_coordinate - valid_y_coordinate[0]))

        return get_index_of_min_item(distances)

    def add_path_point(self, x_coordinate, y_coordinate, time):
        """Adds a point to the attribute 'player_path' and makes sure the point is within the screens bounds"""
        if y_coordinate >= screen_height - self.player2.height:
            y_coordinate = screen_height - self.player2.height

        self.player_path.add_time_point(Point(x_coordinate, y_coordinate), time)

    def go_to_goal(self):
        """Changes the AI's path, so it will move towards the goal"""
        distance_to_goal = self.player2.x_coordinate
        time_to_goal = distance_to_goal / self.player2.velocity

        self.player_path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [],
                                        self.player2.velocity)

        for time in self.get_important_times():
            x_coordinate = self.player2.x_coordinate - time * self.player2.velocity

            self.add_path_point(x_coordinate, self.ball_y_path.get_y_coordinate(time), time)

    def update_ball_data(self):
        """Updates the member of this class 'ball_data' for optimization, so I don't have to keep calling it elsewhere"""

        ball_end_x_coordinate = screen_length - self.ball.length if self.ball.is_moving_right else 0
        self.ball_data = self.get_ball_path_data(self.ball.y_coordinate, self.ball.x_coordinate, ball_end_x_coordinate, self.ball.is_moving_down)
        ball_path, unused, times = self.ball_data

        ball_paths = VelocityPath.get_paths_from_path(ball_path, times)
        self.ball_x_path = ball_paths[0]
        self.ball_right_edge_path = ball_paths[1]
        self.ball_y_path = ball_paths[2]
        self.ball_bottom_path = ball_paths[3]

