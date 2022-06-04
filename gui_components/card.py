from base.colors import red
from base.drawable_objects import GameObject
from base.gui_utility_functions import render_words
from gui_components.text_box import TextBox


class Card(TextBox):
    """A card for wordle that is customizable for the user"""

    is_locked = False
    action = None

    def render(self):
        """Renders the component"""

        # Needs to be here, so doesn't draw over text
        if self.is_locked:
            top_portion = GameObject(self.x_coordinate, self.y_coordinate, self.height * .1, self.length, red)
            bottom_portion = GameObject(self.x_coordinate, top_portion.bottom, self.height - top_portion.height, self.length, self.color)

            top_portion.render()
            bottom_portion.render()

        else:
            GameObject.render(self)

        render_words(self.text, self.font, x_coordinate=self.x_midpoint, y_coordinate=self.y_midpoint,
                     text_color=self.text_color, is_center=True, text_background=self.background_color)

    def run(self):
        """Runs all the code necessary in order for this object to work properly"""

        TextBox.run(self)

        if self.action is not None and self.got_clicked() and self.text != "":
            self.action(self)

    def set_click_action(self, action):
        """Runs the action every time this component is clicked"""

        self.action = action

