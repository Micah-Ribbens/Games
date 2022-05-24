from base.colors import *
from base.events import Event
from base.important_variables import *
from base.utility_functions import key_is_hit
from base.velocity_calculator import VelocityCalculator
from games.minigames.gui.loading_screen import LoadingScreen
from games.minigames.gui.start_screen import StartScreen
from gui.game_selection_screen import GameSelectionScreen
from gui_components.button import Button
from gui_components.screen import Screen


class MainScreen(Screen):
    """The main screen of the application"""

    selection_screen = GameSelectionScreen()
    escape_event = Event()

    def run(self):
        """Runs all the code necessary for this screen to work"""

        self.escape_event.run(key_is_hit(pygame.K_ESCAPE))

        if self.escape_event.is_click():
            self.selection_screen.selected_screen = self.selection_screen

        self.selection_screen.get_selected_screen().run()

    def get_components(self):
        """returns: Component[]; the components that should be rendered"""

        return self.selection_screen.get_selected_screen().get_components()

