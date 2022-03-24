import random
from copy import deepcopy
import pygame

from base.colors import *
from base.dimensions import Dimensions
from base.events import TimedEvent, Event
from base.important_variables import screen_height, screen_length
from base.utility_functions import get_index_of_range
from base.velocity_calculator import VelocityCalculator
from gui_components.button import Button
from gui_components.grid import Grid
from gui_components.intermediate_screens import IntermediateScreens
from gui_components.screen import Screen
from gui_components.sub_screen import SubScreen
from gui_components.text_box import TextBox
from base.utility_classes import HistoryKeeper, Range
from minigames.card_games.word_finder import WordFinder


class Vowel:
    """Stores the percentage that the vowel will show up; i.e. what percent of vowels will be that letter"""

    percentage = 0
    vowel = 0

    def __init__(self, vowel, percentage):
        """Initializes the object"""

        self.percentage, self.vowel = percentage, vowel


class Letter:
    """Stores the actual letter and the amount of that letter"""

    frequency = 0
    letter = ""

    def __init__(self, letter, frequency):
        """Initializes the object"""

        self.frequency, self.letter = frequency, letter


class CardGame(SubScreen):
    """A game where both players have the same cards and the goal of the game is to score 50 before the other player"""

    # Cards Stuff
    player1_current_letters = ""
    player2_current_letters = ""
    all_player1_cards = []
    all_player2_cards = []
    player1_typed_letters = ""
    player2_typed_letters = ""
    player1_score = 0
    player2_score = 0
    number_of_cards = 7
    # Storing Values
    key_to_letter = {pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e", pygame.K_f: "f", pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l", pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o", pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r",pygame.K_s: "s", pygame.K_t: "t", pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x", pygame.K_y: "y", pygame.K_z: "z"}
    is_player1_turn = True
    height_used_up = 0
    length_used_up = 0
    key_events = []
    keys = []
    backspace_event = Event()
    word_finder = WordFinder()
    word_finder = WordFinder()
    max_time = 90 # in seconds
    time_left = max_time
    # GUI
    time_left_field = TextBox("Time Left:", 20, False, white, red)
    player1_score_field = TextBox("Player1 Score", 20, False, white, blue)
    player2_score_field = TextBox("Player2 Score", 20, False, white, purple)
    submit_button = Button("Submit", 20, white, green)
    swap_button = Button("Swap", 20, white, green)
    time_left_field = TextBox("Time Left", 20, False, white, red)
    all_cards = []
    played_cards = []
    components = [player1_score_field, player2_score_field, submit_button, swap_button, time_left_field]
    intermediate_screens = None

    def __init__(self, height_used_up, length_used_up):

        hud_grid_height = VelocityCalculator.give_measurement(screen_height, 10)
        hud_grid = Grid(Dimensions(length_used_up, height_used_up, screen_length - length_used_up, hud_grid_height),
                        None, 1, True)
        hud_components = [self.player1_score_field, self.player2_score_field, self.time_left_field]
        hud_grid.turn_into_grid(hud_components, None, None)

        self.intermediate_screens = IntermediateScreens(height_used_up, length_used_up, 3)

        self.set_up_cards()
        self.keys = self.dict_keys_to_list(self.key_to_letter.keys())
        for x in range(len(self.keys)):
            self.key_events.append(Event())

        # Initializing the text boxes
        for x in range(self.number_of_cards):
            card1 = TextBox("", 20, False, white, blue)
            card2 = TextBox("", 20, False, white, blue)
            card1.set_text_is_centered(True)
            card2.set_text_is_centered(True)
            self.all_cards.append(card1)
            self.played_cards.append(card2)

        self.height_used_up, self.length_used_up = height_used_up, length_used_up

    def dict_keys_to_list(self, dict_keys):
        """ summary: turns dict_keys into a list by iterating over each dict_key and adding it to a list

            params:
                dict_keys: dict_keys; the dict_keys that should be turned into a list

            returns: List of dict_key; the dict_keys as a list
        """
        dict_key_list = []
        for key in dict_keys:
            dict_key_list.append(key)
        return dict_key_list

    def get_cards(self, letters, vowels):
        """returns: List of String; the randomized order of all the letters"""

        all_cards = []
        for letter in letters:
            for x in range(letter.frequency):
                all_cards.append(letter.letter)

        random.shuffle(all_cards)

        for x in range(len(all_cards)):
            if x % 3 == 0:
                all_cards.insert(x, self.get_vowel(vowels))

        return all_cards

    def set_up_cards(self):
        """Sets up all the cards for both players"""

        all_consonants = [Letter("B", 3), Letter("C", 3), Letter("D", 3), Letter("F", 2), Letter("G", 2), Letter("H", 2),
                          Letter("J", 1), Letter("K", 2), Letter("L", 2), Letter("M", 3), Letter("N", 2), Letter("P", 2),
                          Letter("Q", 1), Letter("R", 3), Letter("S", 3), Letter("T", 3), Letter("V", 1), Letter("W", 1),
                          Letter("X", 1), Letter("Y", 2), Letter("Z", 1)]

        vowel_percentages = [Vowel("A", 30), Vowel("E", 30), Vowel("I", 15), Vowel("O", 15), Vowel("U", 10)]
        all_cards = self.get_cards(all_consonants, vowel_percentages)
        self.all_player2_cards, self.all_player1_cards = deepcopy(all_cards), deepcopy(all_cards)
        self.player1_current_letters, self.player2_current_letters = all_cards[0:self.number_of_cards], all_cards[0:self.number_of_cards]

        # So they are all new cards
        self.all_player1_cards = self.all_player1_cards[self.number_of_cards + 1:]
        self.all_player2_cards = self.all_player2_cards[self.number_of_cards + 1:]

    def run(self):
        """Runs all the code for figuring out the score and players moves"""

        self.run_key_events()
        self.player1_score_field.text = f"Player 1 Score: {self.player1_score}"
        self.player2_score_field.text = f"Player 2 Score: {self.player2_score}"
        self.time_left_field.text = f"Time Left: {int(self.time_left)}"
        self.time_left -= VelocityCalculator.time

        if not self.intermediate_screens.is_done():
            self.intermediate_screens.run()

        if self.intermediate_screens.is_done():
            self.intermediate_screens.reset()

        if self.swap_button.got_clicked():
            self.swap_button.text = "Swap" if self.swap_button.text == "Play" else "Play"

        if self.is_player1_turn:
            self.player1_typed_letters += self.get_letters_typed()
            self.player1_typed_letters = self.get_only_possible_letters(self.player1_typed_letters, self.player1_current_letters)

        elif not self.is_player1_turn:
            self.player2_typed_letters += self.get_letters_typed()
            self.player2_typed_letters = self.get_only_possible_letters(self.player2_typed_letters, self.player2_current_letters)

        is_submitted = self.can_submit() and self.submit_button.got_clicked()
        typed_letters = self.player1_typed_letters if self.is_player1_turn else self.player2_typed_letters
        all_letters = self.player1_current_letters if self.is_player1_turn else self.player2_current_letters
        # If the player is swapping they should not get points
        points = 0 if self.is_swapping() else self.get_points(typed_letters)

        if is_submitted and self.is_player1_turn:
            self.player1_score += points

        elif is_submitted and not self.is_player1_turn:
            self.player2_score += points

        if is_submitted and self.is_player1_turn:
            self.player1_current_letters = self.get_current_cards(self.player1_current_letters, self.player1_typed_letters, self.all_player1_cards)
            self.player1_typed_letters = ""

        if is_submitted and not self.is_player1_turn:
            self.player2_current_letters = self.get_current_cards(self.player2_current_letters, self.player2_typed_letters, self.all_player2_cards)
            self.player2_typed_letters = ""

        if is_submitted or self.time_left <= 0:
            player_turn = "Player 1" if self.is_player1_turn else "Player 2"
            longest_word = self.word_finder.get_longest_word(all_letters)
            best_word = f"Best Word: {self.get_uppercase(longest_word)}"
            self.intermediate_screens.display([f"+{points} Points", player_turn, best_word], self.get_times())

            self.is_player1_turn = not self.is_player1_turn
            self.swap_button.text = "Swap"
            self.time_left = self.max_time

    def get_times(self):
        """returns: List of int; the times that the intermediate screens should be displayed"""

        points_time = 0 if self.is_swapping() or self.time_left <= 0 else 1
        player_turn_time = 1
        best_word_time = 0 if self.is_swapping() else 2
        return [points_time, player_turn_time, best_word_time]

    def on_press(self, key):
        letters = "abcdefghijklmnopqrstuvwxyz"
        key = format(key)
        print("CALLED", key)
        can_add = letters.__contains__(key)
        if self.is_player1_turn and can_add:
            self.player1_current_letters += key.upper

        elif can_add:
            self.player2_current_letters += key.upper()

    def get_letters_typed(self):
        """ summary: finds all the keys that was pressed then converts those pressed keys to characters
            params: None
            returns: String; all the letters that have been typed that cycle (typed keys couldn't be held in last cycle)
        """
        letters_pressed = ""
        controls = pygame.key.get_pressed()
        for x in range(len(self.keys)):
            key = self.keys[x]
            key_is_held_in = controls[key]

            letter_was_pressed = key_is_held_in and not self.key_events[x].happened_last_cycle()
            # If the shift key is held in then the letter should be upper case otherwise it shouldn't

            if letter_was_pressed:
                letters_pressed += self.key_to_letter.get(key)

        return letters_pressed
    def get_only_possible_letters(self, typed_letters, player_letters):
        """returns: String; only the letters that could be typed (player_letters has them); all the other letters are removed"""


        if pygame.key.get_pressed()[pygame.K_BACKSPACE] and not self.backspace_event.happened_last_cycle():
            # Removes the last letter
            typed_letters = typed_letters[:-1]

        return_value = ""
        # So it doesn't remove the item from the actual list
        temp = []
        for letter in player_letters:
            temp.append(letter)

        for letter in typed_letters:
            if temp.__contains__(letter.upper()):
                temp.remove(letter.upper())
                return_value += letter.upper()

        return return_value

    def get_components(self):
        """returns: List of Component; all the components that should be displayed"""

        current_letters = self.player1_current_letters if self.is_player1_turn else self.player2_current_letters
        typed_letters = self.player1_typed_letters if self.is_player1_turn else self.player2_typed_letters
        default_color = blue if self.is_player1_turn else purple

        card_colors = self.get_card_colors(current_letters, typed_letters, default_color)
        for x in range(len(current_letters)):
            card: TextBox = self.all_cards[x]
            card.set_color(card_colors[x])
            card.text = current_letters[x]

        played_cards = []
        for x in range(len(typed_letters)):
            card: TextBox = self.played_cards[x]
            card.set_color(default_color)
            card.text = typed_letters[x]
            played_cards.append(card)

        self.set_item_dimensions(self.all_cards, played_cards)

        self.submit_button.background_color = green if self.can_submit() else gray
        self.submit_button.color = green if self.can_submit() else gray
        game_components = self.components + self.all_cards + played_cards
        return game_components if self.intermediate_screens.is_done() else self.intermediate_screens.get_components()

    def set_item_dimensions(self, all_cards, played_cards):
        """Sets the dimensions of the items in all_cards and played_cards"""

        buffer = VelocityCalculator.give_measurement(screen_height, 5)
        # So it takes up half of the remaining screen height
        card_grid_height = (screen_height - self.player1_score_field.bottom - buffer) / 2

        length_buffer = VelocityCalculator.give_measurement(screen_length, 2)
        button_length = VelocityCalculator.give_measurement(screen_length, 15)

        all_cards_grid = Grid(Dimensions(self.length_used_up, self.player1_score_field.bottom + buffer,
                                         screen_length - button_length - self.length_used_up - length_buffer, card_grid_height), None, 1, True)
        all_cards_grid.turn_into_grid(all_cards, None, None)

        last_item = all_cards_grid.dimensions
        self.swap_button.number_set_dimensions(last_item.right_edge + length_buffer, last_item.y_coordinate, button_length, self.all_cards[0].height)

        grid_length = screen_length - self.length_used_up - button_length
        played_cards_grid = Grid(Dimensions(self.length_used_up, last_item.bottom, grid_length - self.length_used_up - length_buffer,
                                            screen_height - last_item.bottom), None, 1, True)
        played_cards_grid.turn_into_grid(played_cards, VelocityCalculator.give_measurement(screen_length, 25), None)

        last_item = played_cards_grid.dimensions
        self.submit_button.number_set_dimensions(last_item.right_edge + length_buffer, last_item.y_coordinate, button_length,
                                                 self.all_cards[0].height)

    def run_key_events(self):
        """Runs all the key events"""
        controls = pygame.key.get_pressed()
        for x in range(len(self.key_events)):
            self.key_events[x].run(controls[self.keys[x]])
        self.backspace_event.run(controls[pygame.K_BACKSPACE])

    def can_submit(self):
        """returns: boolean if the letters can be submitted to get a score"""

        letters = self.player1_typed_letters if self.is_player1_turn else self.player2_typed_letters

        if len(letters) >= 3:
            self.word_finder.is_word(letters)

        is_valid_word = len(letters) >= 2 and self.word_finder.is_word(letters)
        return is_valid_word or self.is_swapping()

    def get_points(self, letters):
        """returns: int; the amount of points that will be scored with those letters"""

        length_to_points = {2: 2, 3: 4, 4: 6, 5: 10, 6: 15, 7: 22}

        return length_to_points.get(len(letters))

    def get_current_cards(self, current_letters, letters, all_cards):
        current_letters_list = self.string_to_list(current_letters)

        for letter in letters:
            current_letters_list.remove(letter)

        new_letters = self.list_to_string(current_letters_list)
        needed_letters = self.number_of_cards - len(new_letters)

        new_letters += self.list_to_string(all_cards[:needed_letters])
        for x in range(needed_letters):
            del all_cards[x]

        return new_letters

    def string_to_list(self, string):
        """returns: List of String; the string as a list"""

        string_list = []
        for ch in string:
            string_list.append(ch)

        return string_list

    def list_to_string(self, string_list):
        "returns: String; the list as a string"

        string = ""
        for item in string_list:
            string += item

        return string

    def get_vowel(self, vowels):
        """returns: String; the vowel that should be added to all player cards"""

        vowel_ranges = []
        total_percent = 0
        for vowel in vowels:
            vowel_ranges.append(Range(total_percent, total_percent + vowel.percentage))
            total_percent += vowel.percentage

        number = random.randint(0, 100)
        return vowels[get_index_of_range(vowel_ranges, number)].vowel


    def get_card_colors(self, current_letters, typed_letters, default_color):
        """Sets the cards colors depending on whether the player has typed it or not"""

        card_colors = []
        typed_letters = self.string_to_list(typed_letters)

        for letter in current_letters:
            if typed_letters.__contains__(letter):
                typed_letters.remove(letter)
                card_colors.append(gray)

            else:
                card_colors.append(default_color)

        return card_colors

    def is_swapping(self):
        """returns: boolean; if the player is currently swapping"""

        return self.swap_button.text == "Play"

    def get_uppercase(self, letters):
        """returns: String; the uppercase form of the letters"""

        return_value = ""

        for letter in letters:
            return_value += letter.upper()

        return return_value