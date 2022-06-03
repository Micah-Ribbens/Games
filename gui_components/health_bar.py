from base.drawable_objects import GameObject
from base.important_variables import screen_height
from base.velocity_calculator import VelocityCalculator
from gui_components.component import Component
from base.colors import *


class HealthBar(Component):
    """A health bar for a game object"""

    game_object = None
    height = VelocityCalculator.give_measurement(screen_height, 3)
    health_remaining_bar = None
    health_gone_bar = None
    set_size = None
    is_addable = False

    def __init__(self, game_object, set_size=None):
        """Initializes the object"""

        self.game_object = game_object
        self.health_remaining_bar = GameObject(0, 0, 0, 0, medium_green)
        self.health_gone_bar = GameObject(0, 0, 0, 0, red)
        self.set_size = set_size if set_size is not None else self.default_set_size
        self.set_size()

    def run(self):
        """Runs all the code necessary for the health bar to work"""

        self.set_size()

    def render(self):
        """Renders the health bar onto the screen"""

        # Setting where the bars should be
        length_ratio = self.length / self.game_object.total_hit_points

        self.health_gone_bar.y_coordinate, self.health_remaining_bar.y_coordinate = self.y_coordinate, self.y_coordinate
        self.health_remaining_bar.height, self.health_gone_bar.height = self.height, self.height
        self.health_remaining_bar.x_coordinate = self.x_coordinate

        self.health_remaining_bar.length = length_ratio * self.game_object.hit_points_left
        self.health_gone_bar.x_coordinate = self.health_remaining_bar.right_edge

        # So there is not a rounding error producing a small part of the health bar being red
        self.health_gone_bar.length = self.length - self.health_remaining_bar.length

        # Rendering
        self.health_remaining_bar.render()

        # Even if the length of it is 0, then it is still being rendered on the screen (a small sliver), so this prevents that
        if self.health_gone_bar.length != 0:
            self.health_gone_bar.render()

    def default_set_size(self):
        """Runs the default way to size the health bar"""

        self.height = self.game_object.height * .1
        self.x_coordinate, self.length = self.game_object.x_coordinate, self.game_object.length
        self.y_coordinate = self.game_object.y_coordinate - self.height




    game_object = None

