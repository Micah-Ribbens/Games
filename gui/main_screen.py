from base.colors import *
from base.dimensions import Dimensions
from base.important_variables import *
from base.utility_functions import percentages_to_numbers
from base.velocity_calculator import VelocityCalculator
from gui.loading_screen import LoadingScreen
from gui.start_screen import StartScreen
from gui_components.button import Button
from gui_components.grid import Grid
from gui_components.screen import Screen
from minigames.quick_draw import QuickDraw


class MainScreen(Screen):
    """The main screen where everything is displayed"""

    start_screen = None
    current_sub_screen = None
    sub_screens = []
    back_button = Button("Back", 20, white, green)

    def __init__(self):
        """Initializes the object"""

        self.back_button.percentage_set_dimensions(0, 0, 20, 10)

        # Creates a little buffer between sub screens and this screen
        height_used_up = self.back_button.height + VelocityCalculator.give_measurement(screen_height, 5)

        self.start_screen = StartScreen(height_used_up, self.back_button.length)
        self.sub_screens = [LoadingScreen(height_used_up, self.back_button.length), self.start_screen]

        self.components = [self.back_button]
        self.current_sub_screen = self.start_screen

    def un_setup(self):
        """ summary: un setups the screen, so the next screen can be set up
            params: None
            returns: None
        """
        game_window.set_screen_visible(self, False)

        for screen in self.sub_screens:
            game_window.set_screen_visible(screen, False)

    def setup(self):
        """ summary: sets up the screen, so it can be displayed on the screen
            params: None
            returns: None
        """

        game_window.set_screen_visible(self, True)

    def run(self):
        """ summary: runs all the necessary logic in order for the main screen to work
            params: None
            returns: None
        """

        if self.back_button.got_clicked():
            self.current_sub_screen = self.start_screen
            self.start_screen.reset()

        if self.current_sub_screen == self.start_screen:
            self.current_sub_screen = self.start_screen.get_selected_screen()

        if self.current_sub_screen is not None:
            self.current_sub_screen.run()

    def get_components(self):
        """returns: List of Component; all the components of the screen that should be displayed"""

        return self.components + self.current_sub_screen.get_components()