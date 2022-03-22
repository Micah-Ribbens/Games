from base.drawable_objects import GameObject
from base.events import Event
from base.utility_classes import HistoryKeeper
from base.utility_functions import percentage_to_number
from base.important_variables import *
import pygame

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

        is_clicked = True
        area = pygame.Rect(self.x_coordinate, self.y_coordinate, self.length,
                           self.height)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        # Otherwise if the mouse is held down this is going to be called over and over again
        if self.click_event.happened_last_cycle():
            is_clicked = False

        if not area.collidepoint(mouse_x, mouse_y) or not mouse_clicked:
            is_clicked = False

        return is_clicked and self.is_visible

    def render(self):
        pass

