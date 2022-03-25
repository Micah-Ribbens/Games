import random

import pygame.key

from base.colors import *
from base.events import TimedEvent, Event
from base.important_variables import screen_height
from gui_components.intermediate_screens import IntermediateScreens
from gui_components.screen import Screen
from gui_components.sub_screen import SubScreen
from gui_components.text_box import TextBox
from base.utility_classes import HistoryKeeper


class QuickDraw(SubScreen):
    """A game where the players have to click a button as quick as they can"""

    # General
    shooting_timed_event = None
    player1_score = 0
    player2_score = 0
    round_number = 1
    player1_shoot_event = Event()
    player2_shoot_event = Event()
    # GUI
    shooting_prompt_field = TextBox("Wait", 60, False, white, red)
    player1_score_field = TextBox("Player1 Score", 25, False, white, blue)
    player2_score_field = TextBox("Player2 Score", 25, False, white, purple)
    intermediate_screens = None
    components = [player2_score_field, player1_score_field, shooting_prompt_field]

    def __init__(self, height_used_up, length_used_up):
        """Initializes the object"""
        percent_height_used_up = (height_used_up / screen_height) * 100
        self.shooting_prompt_field.percentage_set_dimensions(20, percent_height_used_up + 10, 100 - 10 - percent_height_used_up, 60)
        self.player1_score_field.percentage_set_dimensions(0, percent_height_used_up, 50, 10)
        self.player2_score_field.percentage_set_dimensions(50, percent_height_used_up, 50, 10)

        self.player1_score_field.set_text_is_centered(True)
        self.player2_score_field.set_text_is_centered(True)

        self.intermediate_screens = IntermediateScreens(height_used_up, length_used_up, 2)
        self.intermediate_screens.display(["Player Scored", "Round 1"], [0, 1])

    def run(self):
        """runs all the code for figuring out who won and stuff"""

        self.player1_score_field.text = f"Player 1 Score: {self.player1_score}"
        self.player2_score_field.text = f"Player 2 Score: {self.player2_score}"
        self.run_intermediate_screens()
        self.run_shooting()

        controls = pygame.key.get_pressed()

        player1_shoot_key = pygame.K_s
        player2_shoot_key = pygame.K_k
        self.player1_shoot_event.run(controls[player1_shoot_key])
        self.player2_shoot_event.run(controls[player2_shoot_key])

        player1_has_scored = self.player_has_scored(player1_shoot_key, player2_shoot_key, self.player1_shoot_event, self.player2_shoot_event)
        player2_has_scored = self.player_has_scored(player2_shoot_key, player1_shoot_key, self.player2_shoot_event, self.player1_shoot_event)
        self.run_scoring(player1_has_scored, player2_has_scored)

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

    def get_components(self):
        """returns: List of Component; the components that should be displayed"""

        return self.components if self.intermediate_screens.is_done() else self.intermediate_screens.get_components()

    def run_intermediate_screens(self):
        """Runs all the code necessary for intermediate screens"""
        if not self.intermediate_screens.is_done():
            self.intermediate_screens.run()

        if self.intermediate_screens.is_done():
            self.intermediate_screens.reset()

    def run_shooting(self):
        """Runs all the code necessary for the prompt to shoot to display"""

        if self.shooting_timed_event is None:
            time = random.randint(1, 2) + random.random()
            self.shooting_timed_event = TimedEvent(time, False)

        if self.intermediate_screens.is_done():
            self.shooting_timed_event.run(False, True)

        if self.shooting_timed_event.is_done():
            self.shooting_prompt_field.text = "Fire"
            self.shooting_prompt_field.set_color(green)

    def run_scoring(self, player1_has_scored, player2_has_scored):
        """Runs all the code for score keeping"""
        if player1_has_scored:
            self.player1_score += 1

        elif player2_has_scored:
            self.player2_score += 1

        if player1_has_scored or player2_has_scored:
            self.shooting_timed_event = None
            self.shooting_prompt_field.text = "Wait"
            self.shooting_prompt_field.set_color(red)
            self.round_number += 1

            player_message = "Player 1 Has Scored" if player1_has_scored else "Player 2 Has Scored"
            self.intermediate_screens.display([player_message, f"Round {self.round_number}"], [1, 1])

