from base.colors import yellow
from base.drawable_objects import Ellipse
from base.game_movement import GameMovement
from base.important_variables import screen_length, screen_height
from base.velocity_calculator import VelocityCalculator


class DeathBall(Ellipse):
    """A ball that kills the player it touches and if it goes beyond the player's side of the screen also kills the player"""

    is_moving_down = False
    is_moving_right = False
    total_hits_to_change_direction = 5
    hits_left_to_change_direction = total_hits_to_change_direction
    velocity = VelocityCalculator.give_velocity(screen_length, 70)
    velocity_increase = velocity * .2

    def __init__(self):
        """Initializes the object"""

        length = VelocityCalculator.give_measurement(screen_height, 20)
        height = length

        # So it spawns in the middle of the screen
        x_coordinate = (screen_length / 2) - (length / 2)
        y_coordinate = (screen_height / 2) - (height / 2)
        super().__init__(x_coordinate, y_coordinate, height, length, yellow)

    def run(self):
        """Runs all the code in order for this object to work"""

        if self.hits_left_to_change_direction <= 0:
            self.hits_left_to_change_direction = self.total_hits_to_change_direction
            self.is_moving_right = not self.is_moving_right
            self.velocity += self.velocity_increase

        GameMovement.run_projectile_movement(self, self.velocity, self.velocity)




