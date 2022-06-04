from base.drawable_objects import GameObject, Segment
from base.important_variables import (
    screen_height,
    screen_length,
)

from base.velocity_calculator import VelocityCalculator


class Platform(GameObject):
    """The platform that the players can jump onto and interact with"""

    color = (150, 75, 0)
    object_type = "Platform"

    def __init__(self, x_coordinate=0, y_coordinate=0, length=0, height=0, has_supplied_values=False):
        """Initializes the object"""

        if not has_supplied_values:
            height = 150
            length = VelocityCalculator.give_measurement(screen_length, 30)
            super().__init__(100, 500, height, length, (150, 75, 0))

        else:
            super().__init__(x_coordinate, y_coordinate, height, length, (150, 75, 0))

    def render(self):
        """Renders the object onto the screen"""

        green_segment = Segment(
            color=(34, 204, 0),
            percent_down=0,
            percent_right=0,
            percent_length=100,
            percent_height=20
        )
        self.draw_in_segments([green_segment])
