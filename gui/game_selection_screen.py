from base.colors import *
from base.important_variables import *
from base.velocity_calculator import VelocityCalculator
from games.minigames.gui.loading_screen import LoadingScreen
from games.minigames.gui.mini_games_screen import MiniGamesScreen
from games.minigames.gui.start_screen import StartScreen
from gui_components.button import Button
from gui_components.screen import Screen
from gui_components.selection_screen import SelectionScreen


class GameSelectionScreen(SelectionScreen):
    """The Screen that allows you to select all the other games"""

    current_screen = None

    def __init__(self):
        """Initializes the object"""

        screens = [MiniGamesScreen()]
        screen_names = ["Mini Games"]
        super().__init__(0, 0, screens, screen_names)