from base.important_variables import *
from base.velocity_calculator import VelocityCalculator
from games.pong.pong_types.pong_type import PongType
from base.engines import CollisionsFinder
from games.pong.pong_types.normal_pong import NormalPong
from copy import deepcopy


class ShatterPong(PongType):
    normal_pong = None
    
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
        
    def shatter_paddles(self, ball, paddle):
        """ summary: shatters the paddle if the ball hit it

            params:
                ball: Ball; the ball of the game
                paddle: Paddle; the paddle the ball will break if it hits it

            returns: None
        """

        if CollisionsFinder.is_collision(ball, paddle):
            ball_has_hit_top = ball.y_coordinate <= paddle.y_midpoint
            shatter_function = self.shatter_top if ball_has_hit_top else self.shatter_bottom
            shatter_function(paddle)

    def shatter_top(self, paddle):
        """ summary: shatters the top of the paddle

            params:
                paddle: Paddle; the paddle that will be shattered

            returns: None
        """

        height_change = self.ball.bottom - paddle.y_coordinate
        paddle.height -= height_change
        paddle.y_coordinate += height_change

    def shatter_bottom(self, paddle):
        """ summary: shatters the bottom of the paddle

            params:
                paddle: Paddle; the paddle that will be shattered

            returns: None
        """

        paddle.height -= (self.ball.y_coordinate - paddle.y_midpoint)


    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """

        # NormalPong.run() modifies the self.ball, which changes shatter_paddles() collisions, so need to store what the self.ball used to be
        prev_ball = deepcopy(self.ball)

        self.normal_pong.run()
        # Put the shattering below the NormalPong.run(), so it doesn't shatter the paddle messing up the collisions
        self.shatter_paddles(prev_ball, self.player1)
        self.shatter_paddles(prev_ball, self.player2)
        self.draw_game_objects()

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """

        self.player1.height = VelocityCalculator.give_measurement(50, screen_height)
        self.player2.height = VelocityCalculator.give_measurement(50, screen_height)
        self.normal_pong.reset()

