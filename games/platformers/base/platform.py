from base.drawable_objects import GameObject, Segment
from base.important_variables import (
    screen_height,
    screen_length,
)

from base.velocity_calculator import VelocityCalculator

class Platform(GameObject):
    """The platform that the player can jump onto and interact with"""

    color = (150, 75, 0)

    def __init__(self):
        """Initializes the object"""

        height = 100
        length = VelocityCalculator.give_measurement(screen_length, 50)
        super().__init__(100, screen_height, height, length, (150, 75, 0))

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
