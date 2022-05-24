from copy import deepcopy

from base.velocity_calculator import VelocityCalculator
from base.important_variables import *
from base.engines import CollisionsFinder
from games.pong.pong_types.pong_type import PongType
from games.pong.pong_types.normal_pong import NormalPong
from base.quadratic_equations import *


class GravityPong(PongType):
    """Pong with the ball's motion following gravity"""

    normal_pong = None
    time = 0
    physics_equation = None
    base_physics_equation = None
    needed_vertex_increase = 0
    hits = 0
    # The physics equation that would be the 'normal' parabola of the ball- just makes increasing parabola height easier
    bottom_to_top_physics_equation = None

    def __init__(self, player1, player2, ball):
        """ summary: Initializes the PongType with the needed objects to run its methods

            params:
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """

        super().__init__(player1, player2, ball)
        self.normal_pong = NormalPong(player1, player2, ball)
        self.physics_equation = PhysicsEquation()
        self.physics_equation.set_all_variables(250, 1, 250, screen_height - self.ball.height)
        self.ball.y_coordinate = screen_height - self.ball.height
        self.velocity_increase = self.get_velocity_increase(4, 1, 0)
        self.bottom_to_top_physics_equation = deepcopy(self.physics_equation)

    def get_velocity_increase(self, amount_of_hits_to_double, time, vertex):
        """ summary: finds the velocity increase by using the equation d = vit + 1/2 * at^2 where d is displacement, vi is initial velocity,
                     a is acceleration, and t is time

            params:
                amount_of_hits_to_double: int; the amount of hits it takes for the vertex of the equation to double
                time: double; the same time that was used when calling PhysicsEquation.set_all_variables()
                vertex; double; double the vertex (in relation to screen; top is 0 and bottom is 500) that was used when calling PhysicsEquation.set_all_variables()

            returns: double; the velocity increase
        """

        equation = self.physics_equation
        return (vertex - equation.initial_velocity * time - 1/2 * equation.acceleration * pow(time, 2)) / amount_of_hits_to_double

    def ball_collisions(self):
        """ summary: does the ball collisions (interactions with the paddles)
            params: None
            returns: None
        """

        ball_has_collided = CollisionsFinder.is_collision(self.ball, self.player1) or CollisionsFinder.is_collision(self.ball, self.player2)

        if ball_has_collided:
            self.ball.is_moving_right = not self.ball.is_moving_right
            self.needed_vertex_increase += self.velocity_increase

        if CollisionsFinder.is_collision(self.ball, self.player1):
            self.ball.x_coordinate = self.player1.right_edge


        if CollisionsFinder.is_collision(self.ball, self.player2):
            self.ball.x_coordinate = self.player2.x_coordinate - self.ball.length

    def ball_movement(self):
        """ summary: does the horizontal and vertical movement of the ball and the logic that goes into
                     making the ball be affected by gravity

            params: None
            returns: None
        """

        if self.ball.y_coordinate < 0 and self.time > 0:
            self.time = self.get_overshoot_time()

            # Not making it negative because get_velocity_using_displacement gets the seconds number, which is when it is falling
            # Making it already to the sign (+/-) it should be
            initial_velocity = self.physics_equation.get_velocity_using_displacement(-screen_height + self.ball.height)
            self.physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=0)
            self.ball.y_coordinate = 0

        elif self.ball.bottom > screen_height and self.time > 0:
            self.time = self.get_overshoot_time()

            # If the ball has not hit the top of the screen from start -> end it's y coordinate has not changed
            displacement = screen_height - self.ball.height if self.physics_equation.get_vertex() < 0 else 0

            # Making it negative to make it go the opposite direction
            initial_velocity = -self.physics_equation.get_velocity_using_displacement(displacement)
            self.physics_equation.set_variables(initial_velocity=initial_velocity-self.needed_vertex_increase, initial_distance=screen_height-self.ball.height)
            self.needed_vertex_increase = 0
            self.bottom_to_top_physics_equation = deepcopy(self.physics_equation)

            self.ball.y_coordinate = screen_height - self.ball.height

        # IMPORTANT: must be below the if statement(s) otherwise the ball's y_coordinate
        self.time += VelocityCalculator.time

        self.ball.y_coordinate = self.physics_equation.get_distance(self.time)

        x_change = VelocityCalculator.calc_distance(self.ball.forwards_velocity)
        self.ball.x_coordinate += x_change if self.ball.is_moving_right else -x_change

    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """
        self.ball_movement()
        self.ball_collisions()
        self.normal_pong.run_player_movement()

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """
        self.time = 0
        self.ball.y_coordinate = screen_height - self.ball.height
        self.physics_equation.set_all_variables(250, 1, 250, screen_height - self.ball.height)

    def get_overshoot_time(self):
        """returns: double; the amount of time that has passed between when the ball should have hit the floor/ceiling"""

        # Meaning the ball has hit the top of the screen
        if self.physics_equation.get_vertex() <= 0 and self.ball.y_coordinate < 0:
            return_value = self.time - self.physics_equation.get_times_to_point(0)[0]

        # Meaning the ball is coming from hitting the top of the screen
        elif self.physics_equation.initial_velocity > 0 and self.ball.bottom > screen_height:
            # Second number because 0 would be the vertex, so I want the right side of the equation not the left
            return_value = self.time - self.physics_equation.get_times_to_point(screen_height - self.ball.height)[1]

        # Meaning the ball is not coming from the top of the screen: like "normal"
        else:
            return_value = self.time - self.physics_equation.get_full_cycle_time()

        return return_value

    def get_ball_end_y_coordinate(self, ai_x_coordinate):
        """returns: double; the ball's y_coordinate when it reaches the ai"""

        time_to_travel_distance = abs(ai_x_coordinate - self.ball.x_coordinate) / self.ball.forwards_velocity

        if self.physics_equation.get_vertex() > 0:
            return_value = self.get_normal_end_y_coordinate(time_to_travel_distance)

        else:
            return_value = self.get_abnormal_end_y_coordinate(time_to_travel_distance)

        return return_value

    def get_normal_end_y_coordinate(self, time_to_travel_distance):
        """returns: double; the normal end y coordinate of the ball- normal being not bouncing off the ceiling"""

        return_value = None

        time_to_bottom = self.physics_equation.get_full_cycle_time() - self.time

        if time_to_bottom >= time_to_travel_distance:
            return_value = self.physics_equation.get_distance(time_to_travel_distance + self.time)

        else:
            time_to_travel_distance -= time_to_bottom

        new_physics_equation = deepcopy(self.physics_equation)

        new_physics_equation.set_variables(initial_velocity=new_physics_equation.initial_velocity-self.needed_vertex_increase)
        # So the first if statement has not been triggered allowing to move on to new physics equation
        if return_value is None:
            # Removing all the unnecessary cycles for calculation (where it ended where it has started)
            time_to_travel_distance %= new_physics_equation.get_full_cycle_time()
            return_value = new_physics_equation.get_distance(time_to_travel_distance)

        return return_value

    def get_abnormal_end_y_coordinate(self, time_to_travel_distance):
        """returns: double; the end y coordinate when the ball touches the ceiling"""

        return_value = None

        top_to_bottom_physics_equation, time_from_top_to_bottom,  time_from_bottom_to_top = self.get_initial_variables()
        ball_is_going_upwards = self.bottom_to_top_physics_equation == self.physics_equation

        if ball_is_going_upwards and (time_from_bottom_to_top - self.time) >= time_to_travel_distance:
            return_value = self.bottom_to_top_physics_equation.get_distance(self.time + time_to_travel_distance)

        elif ball_is_going_upwards:
            time_to_travel_distance -= (time_from_bottom_to_top - self.time)

        # It is gurranteed now that the ball's position will be at the top of the screen because it if was not then the
        # Previous if statements would have moved it to the top; same type as logic before- the ball has not
        # Reached the other player before hitting the ground
        if (time_from_top_to_bottom - self.time) >= time_to_travel_distance and return_value is None:
            return_value = top_to_bottom_physics_equation.get_distance(time_to_travel_distance)

        elif return_value is None:
            time_to_travel_distance -= (time_from_top_to_bottom - self.time)

        bottom_to_top_physics_equation, top_to_bottom_physics_equation, time_from_top_to_bottom, time_from_bottom_to_top = self.get_end_variables()
        # The code below has return_value is None to make sure the bal has not already reached the other player
        if return_value is None:
            # Removing all the unnecessary cycles for calculation (where it ended where it has started)
            time_to_travel_distance %= (time_from_bottom_to_top + time_from_top_to_bottom)

        if time_from_bottom_to_top >= time_to_travel_distance and return_value is None:
            return_value = bottom_to_top_physics_equation.get_distance(time_to_travel_distance)

        elif return_value is None:
            time_to_travel_distance -= time_from_bottom_to_top

        if return_value is None:
            return_value = top_to_bottom_physics_equation.get_distance(time_to_travel_distance)

        return return_value

    def get_initial_variables(self):
        """returns: [top_to_bottom_physics_equation, time_from_top_to_bottom, time_from_bottom_to_top]"""

        top_to_bottom_physics_equation = deepcopy(self.bottom_to_top_physics_equation)
        initial_velocity = top_to_bottom_physics_equation.get_velocity_using_displacement(-screen_height + self.ball.height)
        top_to_bottom_physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=0)

        time_from_top_to_bottom = top_to_bottom_physics_equation.get_times_to_point(screen_height - self.ball.height)[1]
        time_from_bottom_to_top = self.bottom_to_top_physics_equation.get_times_to_point(0)[0]

        return [top_to_bottom_physics_equation, time_from_top_to_bottom, time_from_bottom_to_top]

    def get_end_variables(self):
        """returns: [bottom_to_top_physics_equation, top_to_bottom_physics_equation, time_from_top_to_bottom, time_from_bottom_to_top]"""
        bottom_to_top_physics_equation = deepcopy(self.bottom_to_top_physics_equation)
        bottom_to_top_physics_equation.set_variables(initial_velocity=bottom_to_top_physics_equation.initial_velocity-self.needed_vertex_increase)

        initial_velocity = bottom_to_top_physics_equation.get_velocity_using_displacement(-screen_height + self.ball.height)
        top_to_bottom_physics_equation = deepcopy(self.bottom_to_top_physics_equation)
        top_to_bottom_physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=0)

        time_from_top_to_bottom = top_to_bottom_physics_equation.get_times_to_point(screen_height - self.ball.height)[1]
        time_from_bottom_to_top = bottom_to_top_physics_equation.get_times_to_point(0)[0]

        return [bottom_to_top_physics_equation, top_to_bottom_physics_equation, time_from_top_to_bottom, time_from_bottom_to_top]

















