from base.colors import *
from base.important_variables import *
from base.velocity_calculator import VelocityCalculator
from games.minigames.gui.loading_screen import LoadingScreen
from games.minigames.gui.mini_games_screen import MiniGamesScreen
from games.minigames.gui.start_screen import StartScreen
from games.platformers.platformer_screen import PlatformerScreen
from games.pong.gui.pong_screen import PongScreen
from games.shooting_games.shooting_game import ShootingGameScreen
from gui_components.button import Button
from gui_components.screen import Screen
from gui_components.selection_screen import SelectionScreen


class GameSelectionScreen(SelectionScreen):
    """The Screen that allows you to select all the other games"""

    current_screen = None

    def __init__(self):
        """Initializes the object"""

        screens = [MiniGamesScreen(), PongScreen(), ShootingGameScreen(), PlatformerScreen()]
        screen_names = ["Mini Games", "Pong Reloaded", "Shooting Game", "Platformer"]
        super().__init__(0, 0, screens, screen_names)