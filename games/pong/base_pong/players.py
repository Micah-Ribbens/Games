from base.colors import *
from base.drawable_objects import GameObject
from base.engines import CollisionsFinder
from base.equations import Point
from base.important_variables import *
from base.path import Path, VelocityPath
from base.utility_classes import Fraction, HistoryKeeper
from base.utility_functions import is_random_chance
from base.velocity_calculator import VelocityCalculator
from games.pong.pong_types.pong_type import PongType


class Paddle(GameObject):
    """The paddle that dimensions can be changed and drawn"""

    can_move_up = True
    can_move_down = True
    base_velocity = VelocityCalculator.give_velocity(screen_height, 1500)
    velocity = base_velocity
    power = 10.5
    attributes = ["x_coordinate", "y_coordinate"]

    def __init__(self):
        """ summary: initializes the paddle with predetermined values
            params: None
            returns: None
        """

        self.y_coordinate = 0
        self.x_coordinate = 0
        self.length = VelocityCalculator.give_measurement(screen_length, 3)
        self.height = VelocityCalculator.give_measurement(screen_height, 33)
        self.color = white
        self.outline_color = red

    def get_top_tip_of_paddle(self):
        return GameObject(self.x_coordinate, self.y_coordinate, self.height * .1, self.length)

    def get_bottom_tip_of_paddle(self):
        tip_height = self.height * .1
        return GameObject(self.x_coordinate, self.bottom - tip_height, tip_height, self.length)

    # def render(self):
    #     paddle_image = pygame.transform.scale(pygame.image.load("images/paddle.png"), (int(self.length), int(self.height)))
    #     game_window.get_window().blit(paddle_image, (self.x_coordinate, self.y_coordinate))


class Player(Paddle):
    """Extends Paddle and provides movement options and a way to change the classes properties"""

    up_key = pygame.K_UP
    down_key = pygame.K_DOWN

    def movement(self):
        """ summary: moves the paddle up and down if those keys were hit
            params: None
            returns: None
        """

        controls = pygame.key.get_pressed()

        if controls[self.up_key] and self.can_move_up:
            self.y_coordinate -= VelocityCalculator.calc_distance(
                self.velocity)

        if controls[self.down_key] and self.can_move_down:
            self.y_coordinate += VelocityCalculator.calc_distance(
                self.velocity)


class AIDifficulty:
    """Stores the data necessary for AI difficulty"""

    min_hits = 0
    hit_percentage = 0
    difficulty_level = 0

    def __init__(self, difficulty_level, min_hits, hit_percentage):
        """Initializes the object"""

        self.difficulty_level = difficulty_level
        self.min_hits, self.hit_percentage = min_hits, hit_percentage

    def should_hit_ball(self, number_of_hits):
        """returns: boolean; if the AI should hit the ball"""

        # Allows for their to be one decimal for hit percentage
        return_value = is_random_chance(Fraction(self.hit_percentage * 10, 1000))

        if number_of_hits <= self.min_hits:
            return_value = True

        return return_value

class AI(Paddle):
    """A player that isn't an actual person- it will be used for a single player option"""

    difficulty_level = 0
    is_going_to_hit_ball = True
    ball = None
    number_of_hits = 0
    pong_type: PongType = None

    # The function that it should run everytime run is called
    action = None

    y_coordinate_should_be_at = 0  # The y_coordinate the computer opponent should move to
    is_moving_down = False
    is_moving = False
    path: VelocityPath = None
    path_is_leftwards = False
    forwards_velocity = VelocityCalculator.give_velocity(400, screen_length)
    ai_difficulty_levels = [AIDifficulty(1, 2, 15), AIDifficulty(2, 2, 25), AIDifficulty(3, 3, 32), AIDifficulty(4, 5, 35),
                            AIDifficulty(5, 5, 42), AIDifficulty(6, 5, 50), AIDifficulty(7, 7, 65), AIDifficulty(8, 7, 70),
                            AIDifficulty(9, 9, 85), AIDifficulty(10, 12, 95)]

    ai_difficulty_level = None
    difficulty_level_index = 0

    ai_path = None

    def __init__(self, difficulty_level, ball):
        """ summary: initializes the object

            params:
                difficulty_level: int; the level of difficulty in the range 1-10
                ball: Ball; the ball that the game is played with

            returns: None
        """
        super().__init__()

        self.difficulty_level_index = difficulty_level - 1
        self.ai_difficulty_level = self.ai_difficulty_levels[self.difficulty_level_index]
        self.ball = ball
        self.action = self.default_run

    def set_pong_type(self, pong_type):
        self.pong_type = pong_type

    def set_action(self, action):
        """ summary: sets the function that should be called every cycle for the computer opponent's movement

            params:
                action: function; the function that should be called every cycle

            returns: None
        """

        self.action = action

    def move_towards_ball(self, ball_y_coordinate, additional_time, is_only_ball=True):
        """ summary: changes the property that tells the computer opponent where to move so it hits the ball

            params:
                ball: Ball; the ball the computer opponent should be moved towards

            returns: None
        """

        # Setting the player's y_midpoint to the ball's y_coordinate
        new_y_coordinate = (ball_y_coordinate - self.height / 2)

        if new_y_coordinate >= screen_height:
            new_y_coordinate = screen_height - self.height

        elif new_y_coordinate <= 0:
            new_y_coordinate = 0

        if is_only_ball:
            self.path = VelocityPath(Point(self.x_coordinate, self.y_coordinate), [], self.velocity)

        print(new_y_coordinate, additional_time)

        self.add_point_to_player_path(new_y_coordinate, additional_time)

    def move_away_from_ball(self, ball_y_coordinate, additional_time, is_only_ball=True):
        """ summary: changes the property that tells the computer opponent where to move so it misses the ball

            params:
                ball: Ball; the ball the computer oponent should be moved away from

            returns: None
        """

        new_y_coordinate = None

        if ball_y_coordinate > screen_height / 2:
            new_y_coordinate = 0

        else:
            new_y_coordinate = screen_height - self.height

        if is_only_ball:
            self.path = VelocityPath(Point(self.x_coordinate, self.y_coordinate), [], self.velocity)

        self.add_point_to_player_path(new_y_coordinate, additional_time)

    def add_point_to_player_path(self, new_y_coordinate, additional_time):
        """Adds the point to the player path, so it will move there"""

        old_y_coordinate = self.path.last_point.y_coordinate
        distance_to_new_y_coordinate = abs(new_y_coordinate - old_y_coordinate)
        time_to_reach_new_y_coordinate = distance_to_new_y_coordinate / self.velocity

        waiting_time = self.get_waiting_time(additional_time, time_to_reach_new_y_coordinate)
        end_time = self.path.last_end_time + additional_time
        time_should_start = end_time - waiting_time - time_to_reach_new_y_coordinate

        # If the ball is coming too quick it should not start moving in negative time
        if waiting_time > 0:
            self.path.add_time_point(Point(self.x_coordinate, old_y_coordinate),
                                     time_should_start)

            self.path.add_point(Point(self.x_coordinate, new_y_coordinate))
            self.path.add_time_point(Point(self.x_coordinate, new_y_coordinate), end_time)

        else:
            self.path.add_time_point(Point(self.x_coordinate, new_y_coordinate), end_time)

    def get_waiting_time(self, additional_time, time_to_reach_new_y_coordinate):
        """returns: double; the time the ai should wait before hitting the ball"""

        max_waiting_time = additional_time - time_to_reach_new_y_coordinate

        # The ai should not wait for no more than a certain amount of time before it hits the ball
        return_value = max_waiting_time if max_waiting_time < .5 else .5

        # Also the AI should not wait at all if it does not have any time to get to the ball
        if max_waiting_time < 0:
            return_value = 0

        return return_value

    def default_run(self):
        """summary: runs the logic for figuring out if the player should hit the ball and the players movement;
            default code if action isn't changed"""

        prev_ball = HistoryKeeper.get_last(self.ball.name)
        prev_ball_is_moving_left = False if prev_ball is None else not prev_ball.is_moving_right

        ball_has_hit_player1 = prev_ball_is_moving_left and self.ball.is_moving_right

        # I want to move the ai if the ball has hit off of another player or it is moving to player2 from respawning
        should_get_ball_coordinates = ball_has_hit_player1 or (self.path is None and self.ball.is_moving_right)

        if self.is_going_to_hit_ball and should_get_ball_coordinates:
            ball_y_coordinate, ball_time_to_ai = self.pong_type.get_ai_data(self.x_coordinate - self.ball.length)
            self.move_towards_ball(ball_y_coordinate, ball_time_to_ai)

        elif not self.is_going_to_hit_ball and should_get_ball_coordinates:
            ball_y_coordinate, ball_time_to_ai = self.pong_type.get_ai_data(self.x_coordinate - self.ball.length)
            self.move_away_from_ball(ball_y_coordinate, ball_time_to_ai)

        self.run_hitting_balls_logic()

    def get_ball_end_coordinates(self, ball_path: Path):
        """ summary: gets the balls end coordinates from the data inside ball_path

            params:
                ball_path: Path; the ball's path

            returns: List of Double; [ball_y_coordinate, ball_bottom]
        """

        ball_end_points = ball_path.get_end_points()
        return [ball_end_points[0].y_coordinate, ball_end_points[1].y_coordinate]

    def run_hitting_balls_logic(self):
        """Runs the logic for figuring out if the computer opponent should hit the next ball"""
        hit_ball_this_cycle = CollisionsFinder.is_collision(self.ball, self)

        if self.path is not None:
            self.x_coordinate, self.y_coordinate = self.path.get_coordinates()
            print(self.path.total_time)

        if hit_ball_this_cycle:
            self.number_of_hits += 1

        if hit_ball_this_cycle:
            self.is_going_to_hit_ball = self.ai_difficulty_level.should_hit_ball(self.number_of_hits)

    def run(self):
        self.action()

    def reset(self):
        """Resets all the variables once a player scores"""

        self.number_of_hits = 0
        self.is_going_to_hit_ball = True
        self.is_moving = False
        self.path = None

    # def render(self):
    #     """renders the ai"""
    #
    #     paddle_image = pygame.transform.scale(pygame.image.load("images/paddle.png"), (int(self.length), int(self.height)))
    #     game_window.get_window().blit(paddle_image, (self.x_coordinate, self.y_coordinate))
    #
    #     if self.path is not None:
    #         self.path.render()

    def add_path(self, path):
        """Makes the AI follow the specified path until it hits the path's end"""

        self.path = path
        self.path_is_leftwards = path.get_end_points()[0].x_coordinate < self.x_coordinate

    def remove_path(self):
        """Makes the AI stop following a path"""

        self.path = None

