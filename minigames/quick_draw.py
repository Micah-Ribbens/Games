import random

import pygame.key

from base.colors import *
from base.events import TimedEvent, Event
from base.important_variables import screen_height
from gui_components.screen import Screen
from gui_components.sub_screen import SubScreen
from gui_components.text_box import TextBox
from base.utility_classes import HistoryKeeper


class QuickDraw(SubScreen):
    """A game where the players have to click a button as quick as they can"""

    shooting_prompt_field = TextBox("Wait", 60, False, white, red)
    player1_score_field = TextBox("Player1 Score", 12, False, white, blue)
    player2_score_field = TextBox("Player2 Score", 12, False, white, purple)
    shooting_timed_event = None
    player1_score = 0
    player2_score = 0
    player1_shoot_event = Event()
    player2_shoot_event = Event()
    components = [player2_score_field, player1_score_field, shooting_prompt_field]

    def __init__(self, height_used_up, length_used_up):
        """Initializes the object"""
        percent_height_used_up = (height_used_up / screen_height) * 100
        self.shooting_prompt_field.percentage_set_dimensions(20, percent_height_used_up + 10, 100 - 10 - percent_height_used_up, 60)
        self.player1_score_field.percentage_set_dimensions(0, percent_height_used_up, 50, 10)
        self.player2_score_field.percentage_set_dimensions(50, percent_height_used_up, 50, 10)

    def run(self):
        """runs all the code for figuring out who won and stuff"""

        self.player1_score_field.text = f"Player 1 Score: {self.player1_score}"
        self.player2_score_field.text = f"Player 2 Score: {self.player2_score}"

        if self.shooting_timed_event is None:
            time = random.randint(1, 2) + random.random()
            self.shooting_timed_event = TimedEvent(time, False)

        self.shooting_timed_event.run(False, True)

        if self.shooting_timed_event.is_done():
            self.shooting_prompt_field.text = "Fire"
            # TODO try figuring out something else, so I don't have to use two lines
            self.shooting_prompt_field.background_color = green
            self.shooting_prompt_field.color = green

        controls = pygame.key.get_pressed()

        player1_shoot_key = pygame.K_s
        player2_shoot_key = pygame.K_k
        self.player1_shoot_event.run(controls[player1_shoot_key])
        self.player2_shoot_event.run(controls[player2_shoot_key])

        player1_has_scored = self.player_has_scored(player1_shoot_key, player2_shoot_key, self.player1_shoot_event, self.player2_shoot_event)
        player2_has_scored = self.player_has_scored(player2_shoot_key, player1_shoot_key, self.player2_shoot_event, self.player1_shoot_event)

        if player1_has_scored:
            self.player1_score += 1

        elif player2_has_scored:
            self.player2_score += 1

        if player1_has_scored or player2_has_scored:
            self.shooting_timed_event = None
            self.shooting_prompt_field.text = "Wait"
            # TODO try figuring out something else, so I don't have to use two lines
            self.shooting_prompt_field.background_color = red
            self.shooting_prompt_field.color = red

    def player_has_scored(self, player_shoot_key, other_player_shoot_key, player_shoot_event, other_player_shoot_event):
        """returns: boolean; if the player has scored; either they hit shoot when screen displayed 'Fire' or the other player hit
        shoot when the screen didn't say 'Fire'"""

        return_value = False
        controls = pygame.key.get_pressed()
        if self.shooting_timed_event.is_done() and controls[player_shoot_key] and not player_shoot_event.happened_last_cycle():
            return_value = True

        if not self.shooting_timed_event.is_done() and controls[other_player_shoot_key] and not other_player_shoot_event.happened_last_cycle():
            return_value = True

        return return_value


