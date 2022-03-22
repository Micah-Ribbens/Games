from base.events import TimedRange
from gui_components.screen import Screen
from gui_components.sub_screen import SubScreen
from gui_components.text_box import TextBox
from base.colors import *
from base.important_variables import *


class LoadingScreen(SubScreen):
    """Screen that shows the loading between mini games"""

    loading_state_field = TextBox("Ready", 36, False, white, background_color)
    components = [loading_state_field]
    loading_range = TimedRange([.5, 1, 1])

    def __init__(self, height_used_up, length_used_up):
        """Initializes the object"""

        percent_height_used_up = (screen_height / height_used_up) * 100

        self.loading_state_field.percentage_set_dimensions(0, percent_height_used_up, 80, 100 - percent_height_used_up)

    def run(self):
        """Runs all the code necessary for the loading screen to load"""

        self.loading_range.run()
        loading_names = ["Ready", "Set", "Go"]

        self.loading_state_field.text = loading_names[self.loading_range.get_current_index()]

    def is_done_loading(self):
        """returns: boolean; if the loading screen is done loading"""

        return self.loading_range.is_done()

    def un_setup(self):
        """Un setups this screen"""

        self.loading_range.reset()
        game_window.set_screen_visible(self, False)
