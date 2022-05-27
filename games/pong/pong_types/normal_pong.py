from base.important_variables import *
from base.velocity_calculator import VelocityCalculator
from base.engines import CollisionsFinder
from games.pong.pong_types.pong_type import PongType
from games.pong.base_pong.players import Paddle, AI
import pygame


class NormalPong(PongType):
    """The normal version of pong"""

    def _ball_collisions(self, ball, player1, player2):
        """ summary: does the collisions of the ball off the players and screen bounds

            params:
                ball: Ball; the ball of the game
                player1: Player; the first player
                player2: Player; the second player

            returns: None
        """

        self.ball_screen_boundary_collisions(ball)

        if CollisionsFinder.is_right_collision(ball, player2):
            CollisionsFinder.is_right_collision(ball, player2)

        if CollisionsFinder.is_left_collision(ball, player1):
            CollisionsFinder.is_left_collision(ball, player1)

        if CollisionsFinder.is_collision(player1, ball):
            self.paddle_collisions(ball, player1)

        if CollisionsFinder.is_collision(player2, ball):
            self.paddle_collisions(ball, player2)

    def ball_collisions(self):
        """ summary: does the ball collisions by calling _ball_collisions()
            params: None
            returns: None
        """

        self._ball_collisions(self.ball, self.player1, self.player2)

    def paddle_collisions(self, ball, paddle):
        """ summary: does the logic for the ball bouncing off of a paddle

            params:
                ball: Ball; the ball that collided with the paddle
                paddle: Paddle; the paddle the ball collided into

            returns: None
        """
        if not CollisionsFinder.is_right_collision(ball, paddle) and not CollisionsFinder.is_left_collision(ball, paddle):
            CollisionsFinder.is_collision(ball, paddle)

        if CollisionsFinder.is_right_collision(ball, paddle):
            ball.x_coordinate = paddle.right_edge
            ball.is_moving_right = True

        elif CollisionsFinder.is_left_collision(ball, paddle):
            ball.x_coordinate = paddle.x_coordinate - ball.length
            ball.is_moving_right = False

        is_collision = CollisionsFinder.is_collision(ball, paddle)

        if CollisionsFinder.is_bottom_collision(ball, paddle):
            ball.tip_hit(paddle.power / 10)
            ball.is_moving_down = True

        elif CollisionsFinder.is_top_collision(ball, paddle):
            ball.tip_hit(paddle.power / 10)
            ball.is_moving_down = False

        elif is_collision:
            ball.middle_hit(paddle.power / 10)

    def ball_movement(self):
        """ summary: does the horizontal and vertical movement of the ball by calling _ball_movement()
            params: None
            returns: None
        """

        self._ball_movement(self.ball)

    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """
        self.ball_movement()
        self.run_player_movement()
        self.ball_collisions()

    def run_player_movement(self):
        """Runs the code that allows the players to move"""
        self.set_paddles_movements(self.player2)
        self.set_paddles_movements(self.player1)
        self.player1.movement()

        if type(self.player2) != AI:
            self.player2.movement()

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """
        self.ball.reset()

    def _ball_movement(self, ball):
        """ summary: does the horizontal and vertical movement of the ball

            params:
                ball: Ball; the ball that should be moved

            returns: None
        """

        distance_change = VelocityCalculator.calc_distance(ball.upwards_velocity)
        ball.y_coordinate += distance_change if ball.is_moving_down else -distance_change
        ball.movement()

    def ball_screen_boundary_collisions(self, ball):
        if ball.bottom >= screen_height:
            distance_change = ball.bottom - screen_height
            ball.is_moving_down = False
            ball.y_coordinate = screen_height - distance_change - ball.height

        if ball.y_coordinate <= 0:
            distance_change = -ball.y_coordinate
            ball.y_coordinate = ball.y_coordinate + distance_change
            ball.is_moving_down = True