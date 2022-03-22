from base.utility_functions import percentage_to_number, percentages_to_numbers
from base.important_variables import *
from gui_components.screen import Screen


class SubScreen:
    """A part of a screen"""

    components = []
    is_visible = True

    def run(self):
        pass

    def get_components(self):
        return self.components
