import random
from copy import deepcopy
import pygame

from base.colors import *
from base.dimensions import Dimensions
from base.events import TimedEvent, Event
from base.important_variables import screen_height, screen_length
from base.utility_functions import get_index_of_range, get_uppercase
from base.velocity_calculator import VelocityCalculator
from gui_components.button import Button
from gui_components.grid import Grid
from gui_components.intermediate_screens import IntermediateScreens
from gui_components.screen import Screen
from gui_components.sub_screen import SubScreen
from gui_components.text_box import TextBox
from base.utility_classes import HistoryKeeper, Range
from minigames.card_games.word_finder import WordFinder
from base.utility_functions import string_to_list, list_to_string
from minigames.card_games.word_game import WordGame


class SpeedGame(WordGame):
    """A word game where you are trying to use the letters as quickly as possible"""

    # General
    max_time = 30
    current_time = max_time
    number_of_cards = 4
    points = 0
    round_number = 1
    cards_gone_through = 1
    typed_letters = ""
    current_letters = ""
    high_score = 0
    # max_vowels = 2; total_letters = 4; needed_possible_words = 2
    all_cards = ['ABCS', 'ABDR', 'ABGR', 'ABLM', 'ABLS', 'ABNR', 'ABNS', 'ABRS', 'ABRT', 'ABST', 'ACHR', 'ACKS', 'ACLM', 'ACLY', 'ACMS', 'ACNS', 'ACPR', 'ACRS', 'ACST', 'ADDS', 'ADDY', 'ADNR', 'ADNW', 'ADRT', 'ADRW', 'ADRY', 'ADSW', 'AFST', 'AGHS', 'AGLS', 'AGNS', 'AGNT', 'AGPS', 'AGST', 'AGSW', 'AHHS', 'AHLT', 'AHMS', 'AHRT', 'AHSW', 'AHTW', 'ALMP', 'ALMS', 'ALPP', 'ALPS', 'ALST', 'ALSW', 'ALSY', 'AMNY', 'AMPR', 'AMPS', 'AMRS', 'AMRT', 'AMRY', 'AMST', 'ANPS', 'ANRT', 'ANST', 'ANSW', 'APRS', 'APRT', 'APRW', 'APSS', 'APST', 'APSW', 'APSY', 'ARST', 'ARTY', 'ARWY', 'ASTV', 'ASTW', 'ASWY', 'EBKR', 'EBST', 'ECHT', 'EDDY', 'EDLW', 'EDNS', 'EDNT', 'EDNY', 'EDSW', 'EFLT', 'EFRS', 'EGLS', 'EHMS', 'EHNW', 'EJST', 'ELLS', 'ELRY', 'ELST', 'ENRT', 'ENST', 'ENSW', 'ENTT', 'ENTW', 'EPRY', 'EPST', 'EPSW', 'ERST', 'ESTT', 'ESTV', 'ESTW', 'IBNS', 'ICHN', 'ICHT', 'ICST', 'IDGR', 'IDKS', 'IDLS', 'IFLT', 'IFST', 'IGNR', 'IGNS', 'IGPR', 'IGRT', 'IHNT', 'IHPS', 'IHST', 'IKLN', 'IKNS', 'IKRS', 'IKSS', 'IKST', 'ILLT', 'ILPS', 'ILST', 'IMSS', 'INPS', 'INST', 'IPST', 'OBLS', 'OBLT', 'OBLW', 'OBRS', 'OBSS', 'OCDL', 'OCDS', 'OCKR', 'OCLT', 'OCST', 'ODGS', 'ODHS', 'ODLT', 'ODNS', 'ODPR', 'OFGL', 'OFLW', 'OFMR', 'OGHS', 'OGLS', 'OGRY', 'OHPS', 'OHST', 'OLNY', 'OLST', 'OLSW', 'OMNR', 'ONSW', 'ONTW', 'OPST', 'ORST', 'ORTY', 'OSTW', 'UBDS', 'UBGR', 'UBHS', 'UBMS', 'UBNS', 'UBRS', 'UBRY', 'UBST', 'UBSY', 'UCDS', 'UCHM', 'UCPS', 'UDST', 'UFRS', 'UGHS', 'UGLP', 'UGLS', 'UGMS', 'UGNS', 'UGST', 'UHMS', 'UHRT', 'UHST', 'UJST', 'ULMP', 'ULST', 'UMST', 'UNPS', 'UNRS', 'UNRT', 'UNST', 'UPSS', 'URST']
    # GUI
    submit_button = Button("Submit", 20, white, green)
    skip_button = Button("Skip", 20, white, green)
    points_field = TextBox("Points", 20, False, white, blue)
    high_score_field = TextBox("High Score", 20, False, white, purple)
    time_field = TextBox("Time", 20, False, white, red)
    components = [submit_button, skip_button, points_field, time_field, high_score_field]

    def __init__(self, height_used_up, length_used_up):
        """Initializes the object"""

        intermediate_screens = IntermediateScreens(height_used_up, length_used_up, 2)
        super().__init__(height_used_up, length_used_up, self.number_of_cards, intermediate_screens)

        hud_grid = Grid(Dimensions(length_used_up, height_used_up, screen_length - length_used_up,
                                   screen_height * .1), None, 1, True)

        hud_grid.turn_into_grid([self.points_field, self.time_field, self.high_score_field], None, None)
        self.run_new_round([1, 0])

    def run(self):
        """Runs all the code necessary in order for this game to work"""
        self.run_key_events()
        self.run_intermediate_screens()

        submit_tried = self.submit_button.got_clicked() or pygame.key.get_pressed()[pygame.K_RETURN]
        is_submitted = self.can_submit() and submit_tried
        is_next_turn = is_submitted or self.skip_button.got_clicked()

        if self.intermediate_screens.is_done():
            self.current_time -= VelocityCalculator.time

        if is_submitted:
            self.points += 1

        if self.skip_button.got_clicked():
            self.points -= 1

        if is_next_turn:
            self.current_letters = self.all_cards[self.cards_gone_through]
            self.cards_gone_through += 1
            self.typed_letters = ""

        if self.current_time <= 0:
            self.run_new_round([1, 1])

        self.typed_letters += self.get_letters_typed()
        self.typed_letters = self.get_only_possible_letters(self.typed_letters, self.current_letters)

    def get_components(self):
        """returns: List of Component; the components that should be rendered"""

        self.points_field.text = f"Points: {self.points}"
        self.time_field.text = f"Time Left: {int(self.current_time)}"
        self.high_score_field.text = f"High Score: {int(self.high_score)}"

        self.set_card_colors(self.typed_letters, self.current_letters, blue)
        played_cards = []

        for x in range(len(self.typed_letters)):
            played_cards.append(self.played_cards[x])

        self.set_item_dimensions(played_cards, self.points_field, self.skip_button, self.submit_button)
        self.submit_button.set_color(green if self.can_submit() else gray)
        game_components = self.components + self.current_cards + played_cards
        return game_components if self.intermediate_screens.is_done() else self.intermediate_screens.get_components()

    def can_submit(self):
        """returns: boolean; if the player can hit the submit button"""

        return super().can_submit(self.typed_letters, self.number_of_cards)

    def run_new_round(self, times):
        """Runs all the code for creating a new round"""

        self.intermediate_screens.display([f"Round Number {self.round_number}", f"Total Points {self.points}"], times)
        random.shuffle(self.all_cards)
        self.round_number += 1

        if self.points > self.high_score:
            self.high_score = self.points

        # Resetting these values back to start values
        self.current_letters = self.all_cards[0]
        self.points, self.cards_gone_through = 0, 1
        self.current_time = self.max_time