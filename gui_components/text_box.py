from copy import deepcopy

from pygame import font
from tkinter import Tk
from base.events import Event
from base.utility_classes import HistoryKeeper
from gui_components.clickable_component import ClickableComponent
from base.utility_functions import render_words, remove_last_ch
from base.drawable_objects import GameObject
from base.dimensions import Dimensions
from base.important_variables import background_color, screen_height, screen_length, game_window
import pygame

pygame.init()
tk = Tk()


class TextBox(ClickableComponent):
    """A box with text inside of it (that text can be altered or can't be depending on the TextBox's attributes
        Shortcuts:
            1. Ctrl + v | Pastes the text inside the clipboard
            2. Ctrl + Backspace | Deletes all the text box's text
            3. Ctrl + e | Expands the text box to the size of the screen
            4. Ctrl + Backspace | Deletes all the text inside the text box
    """

    text = ""
    default_text = ""
    is_editable = False
    font_size = 0
    text_color = None
    background_color = None
    font = None
    # The keyboard key to the actual letter is what the dictionary provides
    key_to_letter = {pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e", pygame.K_f: "f",pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l", pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o", pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r",pygame.K_s: "s", pygame.K_t: "t", pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x", pygame.K_y: "y", pygame.K_z: "z", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9", pygame.K_0: "0", pygame.K_LEFTPAREN: "(", pygame.K_RIGHTPAREN: ")", pygame.K_SPACE: " ", pygame.K_PERIOD: "."}
    keys = None
    key_events = []
    delete_event = None
    ctrl_v_event = None
    expand_key_event = None
    unexpanded_dimensions = None
    previous_components = None
    is_expanded = False

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

    def __init__(self, text, font_size, is_editable, text_color, background_color):
        """ summary: initializes the object

            params:
                text: String; the text that is displayed (can be altered if the text box is editable)
                font_size: int; the size of the font
                is_editable: boolean; if the text inside the text box can be edited
                background_color: tuple; the (Red, Green, Blue) values of the text box's background
            
            returns: None
        """
        self.text, self.font_size = text, font_size
        self.is_editable, self.text_color = is_editable, text_color
        self.background_color = background_color
        self.color = background_color
        self.default_text = text
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        super().__init__()

        one_letter_text = self.font.render("a", True, background_color, background_color)
        one_letter = one_letter_text.get_rect()
        self.font_ch_length = one_letter.width
        self.font_ch_height = one_letter.height

        self.keys = self.dict_keys_to_list(self.key_to_letter.keys())
        for x in range(len(self.keys)):
            self.key_events.append(Event())

        self.delete_event = Event()
        self.ctrl_v_event = Event()
        self.expand_key_event = Event()

    def set_font(self, font_size):
        """ summary: changes the text box's font
            
            params: 
                font_size: int; the size of the text box's font
            
            returns: None
        """
        
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        text = self.font.render("a", True, background_color, background_color)
        text_rect = text.get_rect()
        self.font_ch_length = text_rect.width
        self.font_ch_height = text_rect.height

    def render(self):
        """ summary: renders the text box
            params: None
            returns: None
        """
        
        # Needs to be hear, so doesn't draw over text
        GameObject.render(self)

        current_index = 0
        current_height = self.y_coordinate
        max_index = len(self.text)
        max_text_length = int(self.length / self.font_ch_length)
        words_and_their_indexes = self.get_words_and_their_indexes()
        # It renders line by line, so if the string is too long it won't go off screen
        while current_index < max_index:
            last_cycle_index = current_index
            last_word_index = self.get_last_word_index(words_and_their_indexes, current_index + max_text_length)

            # Code below prevents an endless cycling where the last word is too long, so it can't be rendering
            # Causing a never ending while loop
            if last_cycle_index == last_word_index:
                last_word_index = len(self.text)

            text_being_rendered = self.get_all_words(words_and_their_indexes, current_index, last_word_index)

            render_words(text_being_rendered, self.font, x_coordinate=self.x_coordinate,
                         y_coordinate=current_height, text_color=self.text_color, text_background=self.background_color)

            current_height += self.font_ch_height
            current_index = last_word_index + 1

        # Removing the cursor so it doesn't repeatedly add a cursor
        new_text = ""
        for ch in self.text:
            if ch != "|":
                new_text += ch
        self.text = new_text


    def get_words_and_their_indexes(self):
        """ summary: finds the words and locations of the text box's text
            params: None
            returns: dict {String: int}; the words of the text box's text and the start index of each of those words
        """

        # If the text box is selected it should display a cursor otherwise it shouldn't
        self.text += "|" if self.is_selected and self.is_editable else ""

        word = ""
        words_and_their_indexes = {}
        for x in range(len(self.text)):
            ch = self.text[x]
            if ch == " ":
                words_and_their_indexes[x] = word
                word = ""

            else:
                word += ch

        # The last word won't have a space after it, so I have to add it here
        # Adding words usually added if there is a space
        words_and_their_indexes[len(self.text)] = word
        return words_and_their_indexes

    def get_last_word_index(self, words_and_their_indexes: dict, index):
        """ summary: gets the index of the last word of the text
            if the index is midway through a word it returns the index of the first character of the word before it

            params:
                index: int; the max index that won't overflow the text box's dimensions
                if the text box's length is 9px and the text's length is 10px that would be overflowing
                words_and_indexes: dict {String: int}; the words of the text box's text and the start index of each of those words

            returns: int; the index of the last word
        """

        word_indexes = sorted(words_and_their_indexes.keys())
        max_word_index = 0
        for word_index in word_indexes:
            if word_index <= index and word_index > max_word_index:
                max_word_index = word_index
        return max_word_index

    def get_all_words(self, words_and_their_indexes, start_index, end_index):
        """ summary: gets all the words from the start_index to the end_index
            
            params:
                words_and_their_indexes: dict {String: int}; the words of the text box's text and the start index of each of those words
                start_index: int; the index of the first character in the first word
                end_index: int; the index of the first character in last word

            returns: all the words from the start_index to the end_index
        """
        
        all_indexes = words_and_their_indexes.keys()
        all_words = ""

        for index in all_indexes:
            if index >= start_index and index <= end_index:
                all_words += words_and_their_indexes.get(index) + " "
        return all_words

    def run(self):
        """ summary: runs all the insertion and deletion logic for the text box
            params: None
            returns: None
        """

        ClickableComponent.run(self)

        controls = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        for x in range(len(self.keys)):
            key_event = self.key_events[x]
            key_was_pressed = controls[self.keys[x]]
            key_event.run(key_was_pressed)

        self.delete_event.run(controls[pygame.K_BACKSPACE])

        ctrl_v_clicked = pygame.KMOD_CTRL & mods and controls[pygame.K_v]
        self.ctrl_v_event.run(ctrl_v_clicked)

        expand_key_clicked = controls[pygame.K_e] and mods & pygame.KMOD_CTRL
        self.expand_key_event.run(expand_key_clicked)

        if self.is_selected and self.is_editable:
            self.do_insertion_deletion_logic()

        # If the text box just got selected then the default text shouldn't hinder the user typing
        if self.is_selected and self.text == self.default_text and self.is_editable:
            self.text = ""

        # If the text box got un selected and there is no text then the default text should be displayed
        elif not self.is_selected and self.text == "" and self.is_editable:
            self.text = self.default_text

    def do_insertion_deletion_logic(self):
        """ summary: adds all the typed characters and deletes a character if the backspace was hit
            params: None
            returns: None
        """
        controls = pygame.key.get_pressed()
        mods = pygame.key.get_mods()

        self.text += self.get_letters_typed()

        delete_button_held_in = controls[pygame.K_BACKSPACE] and not self.delete_event.happened_last_cycle()

        if delete_button_held_in and mods & pygame.KMOD_CTRL:
            self.text = ""

        elif delete_button_held_in:
            self.text = remove_last_ch(self.text)

        expand_key_clicked = controls[pygame.K_e] and mods & pygame.KMOD_CTRL

        # TODO fix expanding and unexpanding
        # if expand_key_clicked and self.is_expanded and not self.expand_key_event.is_continuous(expand_key_clicked):
        #     self.unexpand()
        #
        # elif expand_key_clicked and not self.is_expanded and not self.expand_key_event.is_continuous(expand_key_clicked):
        #     self.expand()

    def unexpand(self):
        """ summary: unexpands the textbox and reverts the game window to where it was before the expansion of the text box
            params: None
            returns: None
        """
        for component in self.previous_components:
            game_window.set_visible([component], component.is_visible)

        self.set_dimensions(self.unexpanded_dimensions)
        self.is_expanded = False


    def expand(self):
        """ summary: expands the textbox and stores necessary values to unexpand it
            params: None
            returns: None
        """
        self.is_expanded = True
        self.unexpanded_dimensions = Dimensions(self.x_coordinate, self.y_coordinate, self.length, self.height)
        self.set_dimensions(Dimensions(0, 0, screen_length, screen_height))

        self.previous_components = deepcopy(game_window.screens) + deepcopy(game_window.components)
        game_window.display_components([self])

    def get_letters_typed(self):
        """ summary: finds all the keys that was pressed then converts those pressed keys to characters
            params: None
            returns: String; all the letters that have been typed that cycle (typed keys couldn't be held in last cycle)
        """
        controls = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        letters_pressed = ""
        ctrl_v_clicked = pygame.KMOD_CTRL & mods and controls[pygame.K_v]
        for x in range(len(self.keys)):
            key = self.keys[x]
            key_is_held_in = controls[key]

            # If the user clicked ctrl_v then it shouldn't add 'v' to the text box
            if key == pygame.K_v and ctrl_v_clicked:
                continue
            letter_was_pressed = key_is_held_in and not self.key_events[x].happened_last_cycle()
            # If the shift key is held in then the letter should be upper case otherwise it shouldn't

            if letter_was_pressed and pygame.KMOD_SHIFT & mods:
                letters_pressed += self.key_to_letter.get(key).upper()

            elif letter_was_pressed:
                letters_pressed += self.key_to_letter.get(key)

        if ctrl_v_clicked and not self.ctrl_v_event.happened_last_cycle():
            letters_pressed += tk.clipboard_get()

        return letters_pressed


