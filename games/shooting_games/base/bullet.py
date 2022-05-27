from base.drawable_objects import Ellipse
from base.velocity_calculator import VelocityCalculator
from base.important_variables import *


class Bullet(Ellipse):
    """A projectile that flies across the screen that if hit enough will disappear; can damage other objects also"""

    hits_left_to_destroy = 0
    total_hits_to_destroy = 0
    forwards_velocity = VelocityCalculator.give_velocity(screen_length, 600)
    is_moving_right = False
    is_moving_down = False

    def __init__(self, hits_to_destroy, is_moving_right, x_coordinate, y_coordinate, length, height):
        """Initializes the object"""

        self.hits_left_to_destroy, self.total_hits_to_destroy = hits_to_destroy, hits_to_destroy
        self.is_moving_right, self.x_coordinate = is_moving_right, x_coordinate
        self.y_coordinate, self.length, self.height = y_coordinate, length, height

    def run(self):
        """Runs all the code necessary for this object to work"""

        distance = VelocityCalculator.calc_distance(self.forwards_velocity)
        self.x_coordinate += distance if self.is_moving_right else -distance

