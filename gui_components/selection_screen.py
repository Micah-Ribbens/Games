from math import sqrt
from math import ceil

from base.colors import white, pleasing_green
from base.dimensions import Dimensions
from base.velocity_calculator import VelocityCalculator
from gui_components.button import Button
from gui_components.grid import Grid
from gui_components.sub_screen import SubScreen
from base.important_variables import *


class SelectionScreen(SubScreen):
    """A screen that allows you to select items"""

    components = []
    buttons = []
    selected_screen = None
    screens = []

    def __init__(self, height_used_up, length_used_up, screens, screen_names):
        """Initializes the object"""

        # Resets everything back to the start
        self.buttons, self.components, self.screens = [], [], []

        for screen_name in screen_names:
            self.buttons.append(Button(screen_name, 25, white, pleasing_green))

        # To make the grid as even as possible
        max_columns = ceil(sqrt(len(screen_names)))

        button_grid = Grid(Dimensions(length_used_up, height_used_up, screen_length - length_used_up,
                                      screen_height - height_used_up), max_columns, None, True)

        # So the height buffer is at max 10 percent of the total grid
        max_height_buffer = button_grid.dimensions.height / (10 * max_columns)
        if button_grid.height_buffer > max_height_buffer:
            button_grid.height_buffer = max_height_buffer

        button_grid.turn_into_grid(self.buttons, screen_length / 3, screen_height / 3)
        self.selected_screen = self
        self.screens = screens
        self.components = self.buttons

    def run(self):
        """Runs all the code necessary for the SelectionScreen to work"""

        for x in range(len(self.buttons)):
            button = self.buttons[x]

            if button.got_clicked():
                self.selected_screen = self.screens[x]

    def get_selected_screen(self):
        """returns: SubScreen; the currently selected sub screen"""

        return self.selected_screen

    def reset(self):
        """Resets the screen back to the start"""

        self.selected_screen = self



