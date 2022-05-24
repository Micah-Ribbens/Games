from games.pong.gui.game_modes_screen import GameModesScreen
from games.pong.gui.alter_sizes_screen import AlterSizesScreen
from games.pong.gui.start_screen import StartScreen
from gui_components.button import Button
from gui_components.grid import Grid
from base.colors import *
from base.important_variables import *
from gui_components.screen import Screen
from base.dimensions import Dimensions
from base.utility_functions import percentages_to_numbers


class PongScreen(Screen):
    """The main screen that is booted up from the start"""

    selected_screen = None
    sub_screens = []
    start_screen = None
    start_button = Button("Start", 20, white, green)
    back_button = Button("Back", 20, white, green)
    game_screen = None

    def __init__(self, game_screen):
        """ summary: initializes the object

            params:
                game_screen: Screen; the screen which the game is played on

            returns: None
        """

        self.game_screen = game_screen
        button_grid = self.get_button_grid()
        # Other sub screens are the screens which the start screen will have buttons to jump to;
        # They are screen other than start_screen
        other_sub_screens = [
            AlterSizesScreen(0, button_grid.dimensions.height, self.game_screen),
            GameModesScreen(0, button_grid.dimensions.height),
        ]

        self.start_screen = StartScreen(0, button_grid.dimensions.height, other_sub_screens)

        self.sub_screens = other_sub_screens + [self.start_screen]

        self.components = [self.start_button, self.back_button]
        self.current_sub_screen = self.start_screen

    def run(self):
        """ summary: runs all the necessary logic in order for the main screen to work
            params: None
            returns: None
        """

        if self.back_button.got_clicked():
            game_window.set_screens_visible(self.sub_screens, False)
            game_window.set_screen_visible(self.start_screen, True)
            self.current_sub_screen = self.start_screen

        for button in self.start_screen.sub_screen_buttons:
            if button.got_clicked():
                game_window.set_screens_visible(self.sub_screens, False)
                self.current_sub_screen = self.start_screen.get_sub_screen(button)
                game_window.set_screen_visible(self.current_sub_screen, True)

        if self.current_sub_screen is not None:
            self.current_sub_screen.run()

    def get_button_grid(self):
        """ summary: gets the grid that the buttons to navigates screens should be in
            params: None
            returns: Grid; the grid of the buttons to navigate the screens
        """
        x_coordinate, y_coordinate, length, height = percentages_to_numbers(0, 0, 30, 10, screen_length, screen_height)
        button_grid = Grid(Dimensions(x_coordinate, y_coordinate, length, height), 2, None, True)
        button_grid.turn_into_grid([self.start_button, self.back_button], None, None)
        return button_grid







