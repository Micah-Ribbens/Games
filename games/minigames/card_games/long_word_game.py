import random
from copy import deepcopy
from base.important_variables import *
from base.colors import *
from base.dimensions import Dimensions
from base.utility_functions import get_index_of_range, get_uppercase
from base.velocity_calculator import VelocityCalculator
from gui_components.button import Button
from gui_components.grid import Grid
from gui_components.intermediate_screens import IntermediateScreens
from gui_components.text_box import TextBox
from base.utility_classes import Range
from base.utility_functions import string_to_list, list_to_string
from games.minigames.card_games.word_game import WordGame


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


class CardGame(WordGame):
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
    max_time = 90 # in seconds
    time_left = max_time
    is_player1_turn = True
    # GUI
    time_left_field = TextBox("Time Left:", 20, False, white, red)
    player1_score_field = TextBox("Player1 Score", 20, False, white, blue)
    player2_score_field = TextBox("Player2 Score", 20, False, white, purple)
    swap_button = Button("Swap", 20, white, green)
    time_left_field = TextBox("Time Left", 20, False, white, red)
    all_cards = []
    played_cards = []
    components = [player1_score_field, player2_score_field, swap_button, time_left_field]

    def __init__(self, height_used_up, length_used_up):

        hud_grid_height = VelocityCalculator.give_measurement(screen_height, 10)
        hud_grid = Grid(Dimensions(length_used_up, height_used_up, screen_length - length_used_up, hud_grid_height),
                        None, 1, True)
        hud_components = [self.player1_score_field, self.player2_score_field, self.time_left_field]

        for component in hud_components:
            component.set_text_is_centered(True)

        hud_grid.turn_into_grid(hud_components, None, None)

        intermediate_screens = IntermediateScreens(height_used_up, length_used_up, 3)

        self.set_up_cards()
        self.components.append(self.submit_button)
        super().__init__(height_used_up, length_used_up, self.number_of_cards, intermediate_screens)

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

    def run_getting_letters(self):
        """Runs all the code for getting all the letters the player has typed and keeping only the possible letters"""

        if self.is_player1_turn:
            self.player1_typed_letters += self.get_letters_typed()
            self.player1_typed_letters = self.get_only_possible_letters(self.player1_typed_letters, self.player1_current_letters)

        elif not self.is_player1_turn:
            self.player2_typed_letters += self.get_letters_typed()
            self.player2_typed_letters = self.get_only_possible_letters(self.player2_typed_letters, self.player2_current_letters)

    def run_submission(self):
        """Runs all the code necessary for what to do after submissions"""
        submit_tried = self.submit_button.got_clicked() or pygame.key.get_pressed()[pygame.K_RETURN]
        is_submitted = self.can_submit() and submit_tried
        typed_letters = self.player1_typed_letters if self.is_player1_turn else self.player2_typed_letters
        all_letters = self.player1_current_letters if self.is_player1_turn else self.player2_current_letters
        # If the player is swapping they should not get points
        points = 0 if self.is_swapping() else self.get_points(typed_letters)

        if is_submitted and self.is_player1_turn:
            self.player1_score += points

        elif is_submitted and not self.is_player1_turn:
            self.player2_score += points

        if is_submitted and self.is_player1_turn:
            self.player1_current_letters = self.get_current_cards(self.player1_current_letters,
                                                                  self.player1_typed_letters, self.all_player1_cards)
            self.player1_typed_letters = ""

        if is_submitted and not self.is_player1_turn:
            self.player2_current_letters = self.get_current_cards(self.player2_current_letters,
                                                                  self.player2_typed_letters, self.all_player2_cards)
            self.player2_typed_letters = ""

        if is_submitted or self.time_left <= 0:
            player_turn = "Player 1" if self.is_player1_turn else "Player 2"
            longest_word = self.word_finder.get_longest_word(all_letters)
            best_word = f"Best Word: {get_uppercase(longest_word)}"
            self.intermediate_screens.display([f"+{points} Points", player_turn, best_word], self.get_times())

            self.is_player1_turn = not self.is_player1_turn
            self.swap_button.text = "Swap"
            self.time_left = self.max_time

    def run(self):
        """Runs all the code for figuring out the score and players moves"""

        self.run_key_events()
        self.run_getting_letters()
        self.run_intermediate_screens()
        self.player1_score_field.text = f"Player 1 Score: {self.player1_score}"
        self.player2_score_field.text = f"Player 2 Score: {self.player2_score}"
        self.time_left_field.text = f"Time Left: {int(self.time_left)}"

        if self.intermediate_screens.is_done():
            self.time_left -= VelocityCalculator.time

        if self.swap_button.got_clicked():
            self.swap_button.text = "Swap" if self.swap_button.text == "Play" else "Play"

        self.run_submission()

    def get_times(self):
        """returns: List of int; the times that the intermediate screens should be displayed"""

        points_time = 0 if self.is_swapping() or self.time_left <= 0 else 1
        player_turn_time = 1
        best_word_time = 0 if self.is_swapping() else 2
        return [points_time, player_turn_time, best_word_time]

    def get_components(self):
        """returns: List of Component; all the components that should be displayed"""

        current_letters = self.player1_current_letters if self.is_player1_turn else self.player2_current_letters
        typed_letters = self.player1_typed_letters if self.is_player1_turn else self.player2_typed_letters
        default_color = blue if self.is_player1_turn else purple
        self.set_card_colors(typed_letters, current_letters, default_color)
        played_cards = []

        for x in range(len(typed_letters)):
            played_cards.append(self.played_cards[x])

        self.set_item_dimensions(played_cards, self.player1_score_field, self.swap_button, self.submit_button)

        self.submit_button.set_color(green if self.can_submit() else gray)
        game_components = self.components + self.current_cards + played_cards
        return game_components if self.intermediate_screens.is_done() else self.intermediate_screens.get_components()

    def get_points(self, letters):
        """returns: int; the amount of points that will be scored with those letters"""

        length_to_points = {2: 2, 3: 4, 4: 6, 5: 10, 6: 15, 7: 22}

        return length_to_points.get(len(letters))

    def get_current_cards(self, current_letters, letters, all_cards):
        current_letters_list = string_to_list(current_letters)

        for letter in letters:
            current_letters_list.remove(letter)

        new_letters = list_to_string(current_letters_list)
        needed_letters = self.number_of_cards - len(new_letters)

        new_letters += list_to_string(all_cards[:needed_letters])
        for x in range(needed_letters):
            del all_cards[x]

        return new_letters

    def get_vowel(self, vowels):
        """returns: String; the vowel that should be added to all player cards"""

        vowel_ranges = []
        total_percent = 0
        for vowel in vowels:
            vowel_ranges.append(Range(total_percent, total_percent + vowel.percentage))
            total_percent += vowel.percentage

        number = random.randint(0, 100)
        return vowels[get_index_of_range(vowel_ranges, number)].vowel

    def is_swapping(self):
        """returns: boolean; if the player is currently swapping"""

        return self.swap_button.text == "Play"

    def can_submit(self):
        letters = self.player1_typed_letters if self.is_player1_turn else self.player2_typed_letters
        return super().can_submit(letters, 2) or self.is_swapping()

