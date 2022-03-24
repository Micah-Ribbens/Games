from base.utility_functions import percentage_to_number, percentages_to_numbers
from base.important_variables import *
from gui_components.screen import Screen


class SubScreen:
    """A part of a screen"""

    components = []
    is_visible = True
    length_used_up = 0
    height_used_up = 0

    def __init__(self, height_used_up, length_used_up):
        """Initializes the object"""

        self.length_used_up, self.height_used_up = length_used_up, height_used_up


    def run(self):
        pass

    def get_components(self):
        """returns: List of component; the components that should be displayed"""

        return self.components

