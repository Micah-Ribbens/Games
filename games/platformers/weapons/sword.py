import math

from base.drawable_objects import GameObject
from base.equations import Point, LineSegment
from base.events import TimedEvent
from base.important_variables import screen_length
from base.velocity_calculator import VelocityCalculator
from games.platformers.weapons.weapon import Weapon


# TODO do collision logic for the sword
class Sword(Weapon, LineSegment):
    """Something the player can use to hit enemies with"""

    full_extension_time = 2
    extending_timed_event = None
    start_point = None
    end_point = None
    length = VelocityCalculator.give_measurement(screen_length, 10)
    is_moving_right = False

    def __init__(self, use_key, player):
        """Initializes the object"""

        # Have to add the 'full_extension_time' because the cooldown time starts when the player hits the 'use_key'
        super().__init__(20, 0, use_key, player, self.full_extension_time + .2)
        self.extending_timed_event = TimedEvent(self.full_extension_time, False)

    def run(self):
        """Runs all the code necessary in order for this weapon to work"""

        super().run()
        self.extending_timed_event.run(self.extending_timed_event.current_time > self.extending_timed_event.time_needed, False)

        if not self.extending_timed_event.has_finished():
            self.start_point = Point(self.get_weapon_x_coordinate(0, self.is_moving_right), self.player.projectile_y_coordinate)
            self.end_point = Point(self.start_point.x_coordinate + self.get_horizontal_displacement(),
                                   self.start_point.y_coordinate - self.get_vertical_displacement())

        # If the sword is not extending then it's length should be 0 so it doesn't render or cause collisions
        else:
            self.start_point, self.end_point = Point(0, 0), Point(0, 0)

    def run_player_collision(self, player, index_of_sub_component):
        """Runs what should happen when the player and the weapon collide"""

        player.hit_points -= self.damage

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs what should happen when the weapon and an inanimate object collide"""

        pass

    def run_upon_activation(self):
        """Runs what should happen when the person who plays the game tries to use the weapon"""

        self.extending_timed_event.start()
        self.is_moving_right = self.player.should_shoot_right

    def get_horizontal_displacement(self):
        """returns: double; the horizontal displacement from the player (based on the player's direction)"""

        distance = math.sin(self.get_radians()) * self.length
        return distance if self.is_moving_right else -distance

    def get_vertical_displacement(self):
        """returns: double; the vertical displacement from the player"""

        return math.cos(self.get_radians()) * self.length

    def get_radians(self):
        """returns: double; the radian amount of the sword"""

        fraction_of_full_time = self.extending_timed_event.current_time / self.full_extension_time
        return math.pi * fraction_of_full_time




