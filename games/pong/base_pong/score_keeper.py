import pygame
from base.utility_functions import render_words
from base.important_variables import *
from games.pong.base_pong.ball import Ball


class ScoreKeeper:
    """Provides a way to shore and check if a player has scored"""

    def show_score(player1_score, player2_score):
        """ summary: shows the score of the two players

            params:
                player1_score: int; the score of player 1
                player2_score: int; the score of player 2

            returns: None
        """

        render_words(f"Player 1: {player1_score} Player 2: {player2_score}",
                  pygame.font.Font('freesansbold.ttf', 30), is_center=True, y_coordinate=screen_height*.02, x_coordinate=screen_length/2)

    def player_has_scored(ball: Ball, player_is_leftside: bool):
        """ summary: Figures out if the ball left the screen left or right bounds and if it has if that is the opposite of player_is_leftside

            params:
                ball: Ball; the ball that is used in the game
                player_is_leftside: boolean; the player is on the leftside of the screen
            
            returns: if ball has exited the side of the screen that the player is not on (opposite side of screen is where player scores)
        """

        return ball.x_coordinate >= screen_length if player_is_leftside else ball.x_coordinate <= 0
