from gui_components.clickable_component import ClickableComponent
from gui_components.text_box import TextBox


class Button(TextBox):
    """A clickable component that does an action when clicked"""

    action = None

    def __init__(self, text, font_size, text_color, background_color):
        """ summary: initializes the Button

            params:
                text: String; the text that is displayed on the button
                font_size: int; the size of the button's text
                text_color: tuple; the (Red, Green, Blue) values of the button's text color
                background_color: tuple; the (Red, Green, Blue) values of the button's background
        """

        super().__init__(text, font_size, False, text_color, background_color)

    def add_click_action(self, action):
        """ summary: adds the action to Button.actions; everytime the button is clicked that action will be called

            params:
                action: function; the action that will be called when the button is clicked

            returns: None
        """

        self.action = action

    def run(self):
        """ summary: calls ClickableComponent.run() and calls each action in Button.actions if the button got clicked
            params:None
            returns: None
        """

        ClickableComponent.run(self)

        if self.got_clicked() and self.action is not None:
            self.action()

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text