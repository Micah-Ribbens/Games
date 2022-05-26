from base.equations import Point, LineSegment
from base.important_variables import screen_height
from base.path import Path, PathLine
from base.utility_classes import HistoryKeeper
from games.pong.base_pong.score_keeper import ScoreKeeper
import abc


class PongType(abc.ABC):
    player1 = None
    player2 = None
    ball = None
    is_single_player = False

    def __init__(self, player1, player2, ball):
        """ summary: Initializes the PongType with the needed objects to run its methods
            
            params: 
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """
        self.player1 = player1
        self.player2 = player2
        self.ball = ball

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

    def draw_game_objects(self):
        """ summary: draws all the game objects (paddles and ball) onto the screen
            params: None
            returns: None
        """

        self.player1.render()
        self.player2.render()
        self.ball.render()

    def add_needed_objects(self):
        """ summary: adds all the games objects (paddle and ball) onto the screen
            params: None
            returns: None
        """

        HistoryKeeper.add(self.player1, self.player1.name, True)
        HistoryKeeper.add(self.player2, self.player2.name, True)
        HistoryKeeper.add(self.ball, self.ball.name, True)
    
    def player1_has_scored(self):
        """ summary: finds out if the ball has gone beyond the screens right boundary
            params: None
            returns: boolean; if player1 has scored
        """
        return ScoreKeeper.player_has_scored(self.ball, True)
    
    def player2_has_scored(self):
        """ summary: finds out if the ball has gone beyond the screens left boundary
            params: None
            returns: boolean; if player2 has scored
        """
        return ScoreKeeper.player_has_scored(self.ball, False)

    def set_paddles_movements(self, paddle):
        """ summary: sets all the ways the player can move (up and down)

            params:
                paddle: Paddle; the paddle will have its movement directions it can move set

            returns: None
        """

        paddle.can_move_down = False if paddle.bottom >= screen_height else True
        paddle.can_move_up = False if paddle.y_coordinate <= 0 else True

        if paddle.y_coordinate <= 0:
            paddle.y_coordinate = 0

        if paddle.bottom >= screen_height:
            paddle.y_coordinate = screen_height - paddle.height

    def get_ball_path(self, x_coordinate):
        """ summary: finds the ball's y_coordinate and bottom at the next time it hits the x_coordinate
            IMPORTANT: this function should be called when the ball is going the desired horizontal direction

            params:
                x_coordinate: int; the number that is used to evaluate the ball's path

            returns: Path; the path of the ball from its current x_coordinate to the end x_coordinate
        """

        return self.get_ball_path_from(self.ball.y_coordinate, self.ball.x_coordinate, x_coordinate, self.ball.is_moving_down)

    def get_ball_end_y_coordinate(self, ai_x_coordinate):
        """returns: double; the ball's y_coordinate when it reaches the ai"""

        return self.get_ball_path(ai_x_coordinate).get_end_points()[0].y_coordinate

    def get_ai_data(self, ai_x_coordinate):
        """ summary: calls get_ball_path() to get the ball's path and then just calculates the time for the ball to reach the ai

            params:
                ai_x_coordinate: double; the x coordinate of the ai

            returns: [ball_y_coordinate, ball_time_to_ai]"""
        time_to_travel_distance = abs(ai_x_coordinate - self.ball.x_coordinate) / self.ball.forwards_velocity

        return [self.get_ball_end_y_coordinate(ai_x_coordinate), time_to_travel_distance]

    def get_ball_path_data(self, ball_y_coordinate, ball_x_coordinate, end_x_coordinate, ball_is_moving_down, ball_forwards_velocity=None):
        """returns: [ball_path, ball is moving down at the end, times]"""

        ball_forwards_velocity = ball_forwards_velocity if ball_forwards_velocity is not None else self.ball.forwards_velocity
        path = Path(Point(ball_x_coordinate, ball_y_coordinate), self.ball.height, self.ball.length)
        ball_is_moving_right = end_x_coordinate > ball_x_coordinate

        time_to_travel_distance = abs(end_x_coordinate - ball_x_coordinate) / ball_forwards_velocity
        times = []
        current_time = 0

        while time_to_travel_distance > 0:
            ball_bottom = ball_y_coordinate + self.ball.height

            if ball_is_moving_down:
                displacement = screen_height - ball_bottom

            else:
                displacement = -ball_y_coordinate

            time = abs(displacement / self.ball.upwards_velocity)

            if time_to_travel_distance - time < 0:
                distance = self.ball.upwards_velocity * time_to_travel_distance
                displacement = distance if ball_is_moving_down else -distance
                time = time_to_travel_distance

            # If there is not enough
            else:
                ball_is_moving_down = not ball_is_moving_down

            ball_y_coordinate += displacement

            x_displacement = time * ball_forwards_velocity
            ball_x_coordinate += x_displacement if ball_is_moving_right else -x_displacement

            path.add_point(Point(ball_x_coordinate, ball_y_coordinate))

            current_time += time
            times.append(current_time)
            time_to_travel_distance -= time

        return [path, ball_is_moving_down, times]

    def get_ball_path_from(self, ball_y_coordinate, ball_x_coordinate, end_x_coordinate, ball_is_moving_down):
        """returns: Path; the ball's path from the x_coordinate -> end_x_coordinate; NOTE ball must be moving correct horizontal direction"""

        return self.get_ball_path_data(ball_y_coordinate, ball_x_coordinate, end_x_coordinate, ball_is_moving_down)[0]

    def ball_direction_is_down(self, ball_y_coordinate, ball_x_coordinate, end_x_coordinate, ball_is_moving_down):
        """returns: boolean; if the ball's movement direction is down"""

        return self.get_ball_path_data(ball_y_coordinate, ball_x_coordinate, end_x_coordinate, ball_is_moving_down)[1]
