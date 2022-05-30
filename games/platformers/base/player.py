from math import sqrt

from base.colors import red, light_gray, white
from base.drawable_objects import Segment
from base.events import Event, TimedEvent
from base.game_movement import GameMovement
from base.important_variables import (
    screen_height,
    screen_length
)

from base.engines import *
import pygame

from base.quadratic_equations import PhysicsPath
from base.utility_functions import key_is_hit
from base.velocity_calculator import VelocityCalculator


class Player(GameObject):
    # class States:
    #     """The states the player can be in"""
    #
    #     JUMPING = "Jumping"
    #     RUNNING = "Running"
    #     DECELERATING = "Decelerating"

    # Modifiable numbers
    max_jump_height = VelocityCalculator.give_measurement(screen_height, 40)
    running_deceleration_time = .2
    base_y_coordinate = 0
    base_x_coordinate = 100
    max_velocity = VelocityCalculator.give_velocity(screen_length, 1200)
    time_to_get_to_max_velocity = 1

    # Miscellaneous
    jumping_equation = None
    jumping_event = None
    right_event = None
    left_event = None
    is_runnable = False
    deceleration_event = None
    deceleration_path = None
    acceleration_path = None
    current_velocity = 0

    # Booleans
    can_move_down = True
    can_move_left = True
    can_move_right = True
    is_on_platform = False

    # Keys
    left_key = None
    right_key = None
    jump_key = None
    down_key = None
    attack_key = None

    def __init__(self, left_key, right_key, jump_key, down_key, attack_key):
        """Initializes the object"""

        self.left_key, self.right_key, self.jump_key = left_key, right_key, jump_key
        self.down_key, self.attack_key = down_key, attack_key

        length = VelocityCalculator.give_measurement(screen_length, 5)
        height = VelocityCalculator.give_measurement(screen_height, 15)
        super().__init__(100, screen_height - 200, height, length, white)

        self.jumping_equation = PhysicsPath(self, "y_coordinate", -self.max_jump_height, self.y_coordinate)
        self.jumping_equation.set_initial_distance(self.y_coordinate)
        self.jumping_event, self.right_event, self.left_event = Event(), Event(), Event()
        self.deceleration_event = TimedEvent(self.running_deceleration_time, False)
        self.deceleration_path = PhysicsPath(self, "x_coordinate")
        self.acceleration_path = PhysicsPath()
        self.acceleration_path.set_acceleration(self.time_to_get_to_max_velocity, self.max_velocity)

    def run(self):
        """Runs all the code that is necessary for the player to work properly"""

        self.jumping_event.run(key_is_hit(self.jump_key))
        self.right_event.run(key_is_hit(self.right_key))
        self.left_event.run(key_is_hit(self.left_key))

        self.jumping_equation.run(False, self.jumping_event.is_click())
        GameMovement.set_player_horizontal_movement(self, screen_length, 0)

        if self.right_event.has_stopped() or self.left_event.has_stopped():
            self.decelerate_player(self.right_event.has_stopped())
            self.acceleration_path.reset()

        if self.deceleration_event.has_finished() or self.player_movement_direction_is_same_as_deceleration():
            self.set_current_velocity()
            GameMovement.player_horizontal_movement(self, self.current_velocity, self.left_key, self.right_key)
            self.deceleration_path.reset()
            self.deceleration_event.reset()

        else:
            self.deceleration_event.run(False, False)
            self.deceleration_path.run(False, False, True)

        super().run()

    def render(self):
        """Renders the object onto the screen"""

        eye_color = (0, 0, 255)
        mouth_color = red

        eye1 = Segment(
            color=eye_color,
            percent_down=20,
            percent_right=25,
            percent_length=20,
            percent_height=20)

        eye2 = Segment(
            color=eye_color,
            percent_down=eye1.percent_down,
            percent_right=eye1.right_edge + 10,
            percent_length=eye1.percent_length,
            percent_height=eye1.percent_height)

        mouth = Segment(
            color=mouth_color,
            percent_down=60,
            percent_right=10,
            percent_length=80,
            percent_height=10)

        self.draw_in_segments([eye1, eye2, mouth])

    def set_is_on_platform(self, is_on_platform):
        """Sets the player's is on platform attribute"""

        if self.is_on_platform != is_on_platform and is_on_platform:
            self.jumping_equation.reset()
            self.jumping_equation.set_initial_distance(self.y_coordinate)

        self.is_on_platform = is_on_platform

    def reset(self):
        """Resets the player back to the start of the game"""

        self.x_coordinate = self.base_x_coordinate
        self.y_coordinate = self.base_y_coordinate
        self.jumping_equation.reset()

    def set_y_coordinate(self, y_coordinate):
        """Sets the y coordinate of the player"""

        self.jumping_equation.set_initial_distance(y_coordinate)
        self.y_coordinate = y_coordinate

    def decelerate_player(self, is_moving_right):
        """Makes the player decelerate"""

        self.deceleration_path.initial_distance = self.x_coordinate
        self.deceleration_path.initial_velocity = self.current_velocity if is_moving_right else -self.current_velocity

        # If the player is not at maximum velocity it shouldn't take as long to decelerate
        time_needed = self.running_deceleration_time / (self.max_velocity /  self.current_velocity)

        # Gotten using math; Makes the player stop in the amount of time 'self.running_deceleration_time'
        self.deceleration_path.acceleration = (-self.deceleration_path.initial_velocity)/time_needed

        self.deceleration_event.start()
        self.deceleration_event.time_needed = time_needed
        self.deceleration_path.start()

    def player_movement_direction_is_same_as_deceleration(self):
        """returns: boolean; if the direction the player is moving is equal to the deceleration"""

        deceleration_direction_is_rightwards = self.deceleration_path.acceleration < 0
        return ((deceleration_direction_is_rightwards and key_is_hit(self.right_key)) or
                not deceleration_direction_is_rightwards and key_is_hit(self.left_key))

    def set_current_velocity(self):
        """returns: double; the current velocity of the player"""

        deceleration_has_not_finished = self.deceleration_path.current_time > 0
        self.acceleration_path.run(False, key_is_hit(self.left_key) or key_is_hit(self.right_key), True)

        if deceleration_has_not_finished:
            current_velocity = self.deceleration_path.get_velocity_using_time(self.deceleration_path.current_time)
            # Figuring out the time to get to that velocity, so the player can continue to accelerate to the max velocity
            self.acceleration_path.current_time = sqrt(abs(current_velocity) / self.acceleration_path.acceleration)

        self.current_velocity = self.acceleration_path.get_acceleration_displacement()
        print(self.current_velocity, self.acceleration_path.current_time)

        if self.acceleration_path.current_time > self.time_to_get_to_max_velocity:
            self.current_velocity = self.max_velocity







