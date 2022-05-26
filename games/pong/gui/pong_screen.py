from games.pong.gui.game_modes_screen import GameModesScreen
from games.pong.gui.alter_sizes_screen import AlterSizesScreen
from games.pong.gui.game_screen import GameScreen
from games.pong.gui.pause_screen import PauseScreen
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
    current_screen = None
    pause_screen = None

    def __init__(self):
        """ summary: initializes the object

            params:
                game_screen: Screen; the screen which the game is played on

            returns: None
        """

        self.game_screen = GameScreen()
        self.pause_screen = PauseScreen()
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
        self.current_screen = self

        game_window.set_screens_visible([self.game_screen, self.pause_screen], False)

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
            if button.got_clicked() and self.current_sub_screen == self.start_screen:
                game_window.set_screens_visible(self.sub_screens, False)
                self.current_sub_screen = self.start_screen.get_sub_screen(button)
                game_window.set_screen_visible(self.current_sub_screen, True)

        if self.current_sub_screen is not None:
            self.current_sub_screen.run()

        if self.current_screen != self:
            self.current_screen.run()

        new_screen = self.get_screen()

        if new_screen != self.current_screen:
            self.current_screen.un_setup()
            new_screen.setup()
            game_window.set_screens_visible([self.game_screen, self.pause_screen], False)
            game_window.set_screen_visible(new_screen, True)
            self.current_sub_screen = None

        if new_screen == self and new_screen != self.current_screen:
            self.current_sub_screen = self.start_screen

        self.current_screen = new_screen

    def get_button_grid(self):
        """ summary: gets the grid that the buttons to navigates screens should be in
            params: None
            returns: Grid; the grid of the buttons to navigate the screens
        """
        x_coordinate, y_coordinate, length, height = percentages_to_numbers(0, 0, 30, 10, screen_length, screen_height)
        button_grid = Grid(Dimensions(x_coordinate, y_coordinate, length, height), 2, None, True)
        button_grid.turn_into_grid([self.start_button, self.back_button], None, None)
        return button_grid

    def get_screen(self):
        """returns: Screen; the current screen that should be displayed"""

        action_to_screen = {
            self.game_screen.is_visible and self.game_screen.pause_button.got_clicked(): self.pause_screen,
            self.pause_screen.is_visible and self.pause_screen.continue_game_button.got_clicked(): self.game_screen,
            self.is_visible and self.start_button.got_clicked(): self.game_screen,
            self.pause_screen.is_visible and self.pause_screen.go_to_start_screen_button.got_clicked(): self
        }

        screen = action_to_screen.get(True)
        # If none of the actions are True then action_to_screen.get will return None, so the screen stays
        # As the current_screen

        return screen if screen is not None else self.current_screen

    def get_components(self):
        """returns: Component[]; the components that should be rendered and ran"""

        return_value = self.components

        if self.current_sub_screen is not None:
            return_value = self.current_sub_screen.get_components() + self.components

        if self.current_screen != self:
            return_value = self.current_screen.get_components()

        return return_value






