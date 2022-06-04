import pygame.key

from base.events import Event

from gui_components.screen import Screen
from base.utility_functions import *
from gui_components.selection_screen import SelectionScreen


class NavigationScreen(Screen):
    """A screen that allows you to have a screen with the ability to select other screens and once a screen is selected
    it is possible to navigate to other screens with arrows"""

    current_sub_screen = None
    go_back_event = Event()
    next_screen_event = Event()
    previous_screen_event = Event()
    sub_screens = []
    screen_index = 0
    selection_screen = None

    def __init__(self, sub_screens, sub_screen_names):
        """Initializes the object"""

        self.sub_screens = sub_screens
        self.selection_screen = SelectionScreen(0, 0, sub_screens, sub_screen_names)
        self.current_sub_screen = self.selection_screen

    def get_components(self):
        """returns: List of Component; the components that should be ran and rendered"""

        return self.current_sub_screen.get_components()

    def run(self):
        """Runs everything necessary for this to work"""

        self.go_back_event.run(key_is_hit(pygame.K_ESCAPE))
        self.previous_screen_event.run(key_is_hit(pygame.K_LEFT))
        self.next_screen_event.run(key_is_hit(pygame.K_RIGHT))
        self.selection_screen.run()

        if self.current_sub_screen != self:
            self.current_sub_screen.run()

        # Meaning it can either go forwards or backwards through the sub screens
        is_on_selection_screen = self.current_sub_screen == self.selection_screen

        if not is_on_selection_screen and self.previous_screen_event.is_click():
            self.screen_index = get_prev_index(self.screen_index, len(self.sub_screens) - 1)

        if not is_on_selection_screen and self.next_screen_event.is_click():
            self.screen_index = get_next_index(self.screen_index, len(self.sub_screens) - 1)

        if not is_on_selection_screen:
            self.current_sub_screen = self.sub_screens[self.screen_index]

        a_sub_screen_was_selected = self.selection_screen.selected_screen != self.selection_screen

        if is_on_selection_screen and a_sub_screen_was_selected:
            self.current_sub_screen = self.selection_screen.selected_screen
            self.screen_index = self.sub_screens.index(self.selection_screen.selected_screen)

        if self.go_back_event.is_click():
            self.current_sub_screen = self.selection_screen

            # Have to let the selection screen it is being rendered on the screen otherwise the code doesn't work
            self.selection_screen.selected_screen = self.selection_screen

