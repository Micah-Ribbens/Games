from gui_components.button import Button
from gui_components.grid import Grid
from base.colors import *
from base.velocity_calculator import VelocityCalculator
from base.important_variables import *
from base.dimensions import Dimensions
from base.utility_functions import percentages_to_numbers
from gui_components.sub_screen import SubScreen


class StartScreen(SubScreen):
    """The sub screen that allows the user to jump to other sub screens"""
    selected_screen = None
    other_sub_screens = []
    sub_screen_buttons = []

    def get_sub_screen(self, button_clicked):
        """ summary: gets the sub screen that should currently be displayed after one of the sub screen buttons was clicked

            params:
                button_clicked: Button; the sub screen button that was clicked

            returns: None

        """
        selected_sub_screen = None
        for sub_screen in self.other_sub_screens:
            if button_clicked.text == sub_screen.name:
                selected_sub_screen = sub_screen
        return selected_sub_screen

    def __init__(self, length_used_up, height_used_up, other_sub_screens):
        """ summary: initializes the object

            params:
                length_used_up: int; the length that is used up by the "main screen"
                height_used_up: int; the height that is used up by the "main screen"
                other_sub_screens: List of SubScreen; the other sub screens that this sub screen can access

            returns: None
        """
        self.other_sub_screens = other_sub_screens

#         TODO make it so it doesn't ignore the length and height used up

        for sub_screen in other_sub_screens:
            button = Button(sub_screen.name, 20, white, green)
            self.sub_screen_buttons.append(button)

        self.components = self.sub_screen_buttons

        x_coordinate, y_coordinate, length, height = percentages_to_numbers(0, 20, 100, 90, screen_length,
                                                                            screen_height)
        sub_screen_button_grid = Grid(Dimensions(x_coordinate, y_coordinate, length, height), 3, None, True)

        max_height = VelocityCalculator.give_measurement(screen_height, 20)
        sub_screen_button_grid.turn_into_grid(self.sub_screen_buttons, None, max_height)






        
        
                

