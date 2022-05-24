from base.important_variables import *
from base.engines import CollisionsFinder
from games.pong.pong_types.pong_type import PongType
from games.pong.pong_types.normal_pong import NormalPong
from games.pong.base_pong.players import Paddle
from base.velocity_calculator import VelocityCalculator
from base.utility_classes import HistoryKeeper


class MiddlePaddlePong(PongType):
    """A pong type where a middle paddle goes up and down"""

    middle_paddle = Paddle()
    normal_pong = None

    def __init__(self, player1, player2, ball):
        """ summary: initializes the object

            params:
                player1: Player; the first player
                player2: Player; the second player
                ball: Ball; the ball of pong

            returns: None
        """

        self.normal_pong = NormalPong(player1, player2, ball)
        super().__init__(player1, player2, ball)

        self.middle_paddle.x_coordinate = screen_length // 2
        self.middle_paddle.y_coordinate = 0
        self.middle_paddle.name = "middle_paddle"
        self.middle_paddle.height = VelocityCalculator.give_measurement(screen_height, 33)
        self.middle_paddle.is_moving_down = False
        self.middle_paddle.power = 10.5

    def middle_paddle_movement(self):
        """ summary: moves the middle paddle up and down
            params: None
            returns: None
        """

        if self.middle_paddle.bottom >= screen_height:
            self.middle_paddle.is_moving_down = False
        if self.middle_paddle.y_coordinate <= 0:
            self.middle_paddle.is_moving_down = True
        y_change = VelocityCalculator.calc_distance(self.middle_paddle.velocity)
        self.middle_paddle.y_coordinate += y_change if self.middle_paddle.is_moving_down else -y_change

    def ball_collisions(self):
        """ summary: does the ball collisions for the middle paddle
            params: None
            returns: None
        """

        # Ball collisions changes colors if it hits middle_paddle
        # and I won't to change it back to color before hitting it
        if CollisionsFinder.is_collision(self.ball, self.middle_paddle):
            self.normal_pong.paddle_collisions(self.ball, self.middle_paddle)

    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """

        self.normal_pong.run()
        self.middle_paddle.render()
        self.ball_collisions()
        self.middle_paddle_movement()
        self.ball_collisions()

    def add_needed_objects(self):
        """ summary: adds all the objects to the HistoryKeeper
            params: None
            returns: None
        """

        super().add_needed_objects()
        HistoryKeeper.add(self.middle_paddle, self.middle_paddle.name, True)

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """
        self.normal_pong.reset()
