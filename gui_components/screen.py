from gui_components.component import Component


class Screen:
    """Is the only thing that shows on the window at a time"""

    components = []
    current_sub_screen = None
    is_visible = True

    def get_components(self):
        """ summary: gets all the screen's components
            params: None
            returns: all the screen's components
        """
        sub_screen_components = []

        if self.current_sub_screen is not None:
            sub_screen_components += self.current_sub_screen.get_components()

        return self.components + sub_screen_components

    def render(self):
        pass

    def setup(self):
        pass

    def run(self):
        pass

    def un_setup(self):
        pass
