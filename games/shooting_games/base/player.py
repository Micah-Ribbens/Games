import pygame

from base.drawable_objects import GameObject
from base.events import TimedRange, TimedEvent
from base.game_movement import GameMovement
from base.important_variables import screen_height, screen_length
from base.utility_classes import HistoryKeeper
from base.utility_functions import key_is_hit
from base.velocity_calculator import VelocityCalculator
from games.shooting_games.base.bullet import Bullet
from base.colors import *


class Player(GameObject):
    """The player of the game that can shot and stuff"""

    turret = None
    turret_height = 0
    velocity = VelocityCalculator.give_velocity(screen_height, 1500)
    is_facing_right = False
    turret_movement_velocity = VelocityCalculator.give_velocity(screen_height, 700)

    # Keys
    left_key = None
    right_key = None
    up_key = None
    down_key = None
    move_turret_key = None
    shoot_key = None

    # Movement directions
    can_move_left = True
    can_move_right = True
    can_move_down = True
    can_move_up = True

    shooting_timed_range = None
    bullets = []

    # Waiting Events
    wait_to_shoot_event = None
    stun_event = None
    base_color = None
    invincibility_event = None

    def __init__(self, left_key, right_key, up_key, down_key, move_turret_key, shoot_key):
        """Initializes the object"""

        self.left_key, self.right_key, self.up_key = left_key, right_key, up_key
        self.down_key, self.move_turret_key, self.shoot_key = down_key, move_turret_key, shoot_key

        length = VelocityCalculator.give_measurement(screen_length, 4)
        height = VelocityCalculator.give_measurement(screen_height, 20)
        super().__init__(0, screen_height / 2, height, length)
        self.turret_height = height * .2
        self.name = id(self)

        self.turret = GameObject(self.x_coordinate - self.length, self.y_midpoint, self.turret_height, self.length)

        # Adding these variables allows for the use of helpful functions
        self.turret.can_move_up, self.turret.can_move_down = False, False

        # The player can hold the key in as long as they want if the projectile is fully charged
        self.shooting_timed_range = TimedRange([.2, .5, float("inf")])
        self.wait_to_shoot_event = TimedEvent(.2, False)
        self.stun_event = TimedEvent(.2, False)
        self.invincibility_event = TimedEvent(1, False)

        self.base_color = black

    def run(self):
        """Runs all the code necessary for this player to work properly"""

        self.wait_to_shoot_event.run(False, len(self.bullets) != 0)
        self.bullets = []

        if not self.stun_event.has_finished():
            self.stun_event.run(False, False)
            self.color = white

        # self.invincibility_event.run(False, self.stun_event.current_time >= self.stun_event.time_needed)

        if self.stun_event.has_finished():
            self.run_movement_and_shooting()
            self.stun_event.reset()
            self.color = self.base_color

    def run_movement_and_shooting(self):
        """Runs the movement and shooting of the player"""

        if key_is_hit(self.right_key):
            self.is_facing_right = True

        elif key_is_hit(self.left_key):
            self.is_facing_right = False

        GameMovement.player_horizontal_movement(self, self.velocity, self.left_key, self.right_key)
        GameMovement.set_player_vertical_movement(self.turret, self.bottom, self.y_coordinate)

        self.turret.x_coordinate = self.right_edge if self.is_facing_right else self.x_coordinate - self.length

        if key_is_hit(self.move_turret_key):
            GameMovement.player_vertical_movement(self.turret, self.turret_movement_velocity, self.up_key, self.down_key)

        else:
            # So the turret moves with the player
            GameMovement.player_vertical_movement(self.turret, self.velocity, self.up_key, self.down_key, self.can_move_up, self.can_move_down)
            GameMovement.player_vertical_movement(self, self.velocity, self.up_key, self.down_key)

        if not key_is_hit(self.shoot_key):
            self.bullets = self.get_bullets()
            self.shooting_timed_range.reset()

        else:
            self.shooting_timed_range.run()

    def render(self):
        """Renders the object on the screen"""

        GameObject.render(self)
        self.turret.render()

    def get_bullets(self):
        """returns: Bullet[]; the bullet that has been shot"""

        return_value = []

        if self.shooting_timed_range.current_time != 0 and self.wait_to_shoot_event.has_finished():
            bullet_health = self.shooting_timed_range.get_current_index() + 1
            bullet_size = VelocityCalculator.give_measurement(screen_height, 3) * bullet_health
            self.wait_to_shoot_event.reset()
            ball_x_coordinate = self.turret.right_edge if self.is_facing_right else self.turret.x_coordinate

            bullet = Bullet(bullet_health, self.is_facing_right, ball_x_coordinate,
                            self.turret.y_midpoint, bullet_size, bullet_size)

            bullet.color = self.color
            return_value = [bullet]

        return return_value

    def stun(self, stun_time):
        """Stuns the player for the amount of time specified"""

        # if self.invincibility_event.is_started:
        #     print("BREAK")
        # if self.invincibility_event.has_finished():
        self.stun_event.time_needed = stun_time
        self.stun_event.current_time = VelocityCalculator.time
        self.stun_event.start()

    def set_color(self, color):
        """Sets the color of this player"""

        self.base_color = color



