from base.colors import *
from base.dimensions import Dimensions
from base.events import Event
from base.important_variables import *
from base.utility_functions import string_to_list
from base.velocity_calculator import VelocityCalculator
from gui_components.button import Button
from gui_components.grid import Grid
from gui_components.intermediate_screens import IntermediateScreens
from gui_components.sub_screen import SubScreen
from gui_components.text_box import TextBox
from games.minigames.card_games.word_finder import WordFinder


class WordGame(SubScreen):
    # Key Stuff
    key_to_letter = {pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e", pygame.K_f: "f", pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l", pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o", pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r",pygame.K_s: "s", pygame.K_t: "t", pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x", pygame.K_y: "y", pygame.K_z: "z"}
    key_events = []
    keys = []
    backspace_event = Event()
    # Other Stuff
    word_finder = WordFinder()
    intermediate_screens: IntermediateScreens = None
    # GUI
    current_cards = []
    played_cards = []
    submit_button = Button("Submit", 20, white, green)

    def __init__(self, height_used_up, length_used_up, number_of_cards, intermediate_screens):
        """Initializes the object"""

        self.key_events, self.current_cards, self.played_cards = [], [], []

        self.keys = self.dict_keys_to_list(self.key_to_letter.keys())
        for x in range(len(self.keys)):
            self.key_events.append(Event())

        # Initializing the text boxes
        for x in range(number_of_cards):
            card1 = TextBox("", 20, False, white, blue)
            card2 = TextBox("", 20, False, white, blue)
            card1.set_text_is_centered(True)
            card2.set_text_is_centered(True)
            self.current_cards.append(card1)
            self.played_cards.append(card2)

        self.height_used_up, self.length_used_up = height_used_up, length_used_up
        self.intermediate_screens = intermediate_screens

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

    def run_key_events(self):
        """Runs all the key events"""

        controls = pygame.key.get_pressed()
        for x in range(len(self.key_events)):
            self.key_events[x].run(controls[self.keys[x]])

        self.backspace_event.run(controls[pygame.K_BACKSPACE])

    def can_submit(self, letters, needed_length):
        """returns: boolean if the letters can be submitted to get a score"""

        is_valid_word = len(letters) >= needed_length and self.word_finder.is_word(letters)
        return is_valid_word

    def get_card_colors(self, current_letters, typed_letters, default_color):
        """Sets the cards colors depending on whether the player has typed it or not"""

        card_colors = []
        typed_letters = string_to_list(typed_letters)

        for letter in current_letters:
            if typed_letters.__contains__(letter):
                typed_letters.remove(letter)
                card_colors.append(gray)

            else:
                card_colors.append(default_color)

        return card_colors

    def set_card_colors(self, typed_letters, current_letters, default_color):
        """Sets the cards colors to make it look good"""

        for x in range(len(typed_letters)):
            card: TextBox = self.played_cards[x]
            card.set_color(default_color)
            card.text = typed_letters[x]

        card_colors = self.get_card_colors(current_letters, typed_letters, default_color)
        for x in range(len(current_letters)):
            card: TextBox = self.current_cards[x]
            card.set_color(card_colors[x])
            card.text = current_letters[x]

    def run_intermediate_screens(self):
        """Runs all the logic necessary for intermediate screens"""

        if not self.intermediate_screens.is_done():
            self.intermediate_screens.run()

        if self.intermediate_screens.is_done():
            self.intermediate_screens.reset()

    def set_item_dimensions(self, played_cards, last_item, all_cards_button, played_cards_button):
        """Sets the dimensions of the GUI components"""

        buffer = VelocityCalculator.give_measurement(screen_height, 5)
        # So it takes up half of the remaining screen height
        card_grid_height = (screen_height - last_item.bottom - buffer) / 2

        length_buffer = VelocityCalculator.give_measurement(screen_length, 2)
        button_length = VelocityCalculator.give_measurement(screen_length, 15)

        all_cards_grid = Grid(Dimensions(self.length_used_up, last_item.bottom + buffer,
                                         screen_length - button_length - self.length_used_up - length_buffer, card_grid_height), None, 1, True)
        all_cards_grid.turn_into_grid(self.current_cards, None, None)

        last_item = all_cards_grid.dimensions
        all_cards_button.number_set_dimensions(last_item.right_edge + length_buffer, last_item.y_coordinate, button_length, self.current_cards[0].height)

        grid_length = screen_length - self.length_used_up - button_length
        played_cards_grid = Grid(Dimensions(self.length_used_up, last_item.bottom, grid_length - self.length_used_up - length_buffer,
                                            screen_height - last_item.bottom), None, 1, True)
        played_cards_grid.turn_into_grid(played_cards, VelocityCalculator.give_measurement(screen_length, 25), None)

        last_item = played_cards_grid.dimensions
        played_cards_button.number_set_dimensions(last_item.right_edge + length_buffer, last_item.y_coordinate, button_length,
                                                 self.current_cards[0].height)