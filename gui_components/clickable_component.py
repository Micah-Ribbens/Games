import pygame

from base.events import Event
from gui_components.component import Component


class ClickableComponent(Component):
    """A component that can be clicked"""

    click_event = None
    amount_clicked = None

    def __init__(self):
        """ summary: initializes the component
            params: None
            returns: None
        """
        self.click_event = Event()
        self.amount_clicked = []

    def run(self):
        """ summary: runs this object's click event (used to make sure an object isn't clicked continuously)
            things that inherit from this class must call this function in order for clicking to work properly
        """

        mouse_clicked = pygame.mouse.get_pressed()[0]
        self.click_event.run(mouse_clicked)

    def got_clicked(self):
        """ summary: checks if the user has their mouse of the component, clicked it, and that click didn't happen last cycle also
            params: None
            returns: boolean; if the component got clicked
        """

        mouse_clicked = pygame.mouse.get_pressed()[0]

        # return statement here for performance because the rest of the code does not have to be ran if this is True
        if not self.is_visible or self.click_event.happened_last_cycle() or not mouse_clicked:
            return False

        is_clicked = True
        area = pygame.Rect(self.x_coordinate, self.y_coordinate, self.length,
                           self.height)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if not area.collidepoint(mouse_x, mouse_y):
            is_clicked = False

        return is_clicked

    def render(self):
        pass

