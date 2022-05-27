from base.utility_classes import HistoryKeeper
from base.drawable_objects import Ellipse
from base.velocity_calculator import VelocityCalculator
from base.important_variables import *
from base.colors import *
from base.utility_classes import Fraction


class Ball(Ellipse):
    """ The elliptical object that moves across the screen"""

    is_moving_right = False
    is_moving_down = True
    # TODO change me back to 300
    base_forwards_velocity = VelocityCalculator.give_velocity(screen_length, 350)
    forwards_velocity = base_forwards_velocity
    # Forwards and upwards velocity start out as the same number
    upwards_velocity = base_forwards_velocity
    # Normal meaning what the velocities would be if there was no tip hits affected the ball
    normal_upwards_velocity = base_forwards_velocity
    normal_forwards_velocity = base_forwards_velocity
    can_move = True
    height = VelocityCalculator.give_measurement(screen_height, 5)
    time_since_ground = 0
    attributes = ["x_coordinate", "y_coordinate", "length", "height", "forwards_velocity"]
    length = VelocityCalculator.give_measurement(screen_height, 5)
    active_tip_hits = 0
    name = "ball"
    # Everytime there is a tip hit then the forwards_velocity will be multiplies by this fraction
    # If the fractions was 1/2 for instance then everytime there is a tip hit then the forwards_velocity would halve
    # That other half would be added to the upwards velocity and if it is a middle hit the tip hits would be "reversed"
    forwards_velocity_multiplier: Fraction = Fraction(3, 4)

    def __init__(self):
        """ summary: initializes the object by setting the length and name to a value
            params: None
            returns: None
        """

        self.length = VelocityCalculator.give_measurement(screen_height, 5)
        self.name = "ball"

    def reset(self):
        """ summary: Resets the variables to where they were before the game was played (ball moving and paddles hitting it)
            params: None
            returns: None
        """

        self.x_coordinate = screen_length // 2
        self.y_coordinate = screen_height // 2
        self.forwards_velocity = self.base_forwards_velocity
        self.upwards_velocity = self.base_forwards_velocity
        self.normal_forwards_velocity = self.base_forwards_velocity
        self.normal_upwards_velocity = self.base_forwards_velocity
        self.color = white

    def movement(self):
        """ summary: moves the ball x_coordinate based upon the ball's forwards_velocity and the time that has
            passed that cycle

            params: None
            returns: None
        """

        x_change = VelocityCalculator.calc_distance(self.forwards_velocity)
        self.x_coordinate += x_change if self.is_moving_right else -x_change
    
    def tip_hit(self, paddle_hit_multiplier):
        """ summary: The ball's forwards forwards_velocity goes down by a fraction (is multiplied by a fraction less than 1) the amount
        that the forwards_velocity goes down is how much the upwards_velocity goes up

            params:
                paddle_hit_multiplier: int; the number that both upwards and forwards velocity are multiplied by

            returns: None
        """

        # Every tip hit makes the forwards_velocity go down and the amount that the forwards velocity goes does is how much the upwards velocity
        # Will go up and that will be "reverted" if there is a middle hit; so if every time theirs a tip hit the forwards velocity is multiplied
        # By 1/2 that would mean if there were 2 active tip hits that would mean the forwards velocity would be 1/4 of what it is normally
        # The remaining 3/4 (1 - 1/4 = 3/4) would be added to the upwards velocity
        self.active_tip_hits += 1
        fraction_of_forwards_velocity = self.forwards_velocity_multiplier.get_fraction_to_power(self.active_tip_hits)
        self.change_velocities(fraction_of_forwards_velocity)

        self.normal_forwards_velocity *= paddle_hit_multiplier
        self.normal_upwards_velocity *= paddle_hit_multiplier
    
    def middle_hit(self, paddle_hit_multiplier):
        """ summary: Reverts what the last tip hit did (made forwards_velocity go down and upwards_velocity go up) if not all of the 
                    tip hits had been reverted

            params:
                paddle_hit_multiplier: int; the number that both the forwards_velocity and upwards_velocity are multiplied by
    
            returns: None
        """

        # If there are active hits one of them must be reverted
        if self.active_tip_hits >= 1:
            # The minus one will "revert" an active tip hit
            fraction_of_forwards_velocity = self.forwards_velocity_multiplier.get_fraction_to_power(self.active_tip_hits - 1)
            self.change_velocities(fraction_of_forwards_velocity)
        
        self.normal_forwards_velocity *= paddle_hit_multiplier
        self.normal_upwards_velocity *= paddle_hit_multiplier
        # The number of active tip hits can't be in the negatives
        if self.active_tip_hits >= 1:
            self.active_tip_hits -= 1

    def change_velocities(self, fraction_of_forwards_velocity):
        """ summary: a method that is a helper function to tip_hit() and middle_hit() and it changes the velocities based on what
            the fraction_of_forwards_velocity is; the forwards velocity is multiplied by that fraction (fraction is less than 1) and the
            upwards_velocity goes up by how much the forwards_velocity went down

            params:
                fraction_of_forwards_velocity: Fraction; the number that the forwards_velocity is multiplied by
                
            returns: None
        """

        self.forwards_velocity = self.normal_forwards_velocity * fraction_of_forwards_velocity.get_number()

        # What the forwards_velocity lost from the fraction will be added to upwards_velocity
        added_velocity = self.normal_forwards_velocity * fraction_of_forwards_velocity.get_fraction_to_become_one().get_number()
        self.upwards_velocity = self.normal_upwards_velocity + added_velocity