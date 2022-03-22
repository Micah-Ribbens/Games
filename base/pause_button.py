from gui_components.clickable_component import ClickableComponent
from base.important_variables import (
    screen_length,
    screen_height,
    game_window
)
from base.velocity_calculator import VelocityCalculator
import pygame
pygame.init()

class PauseButton(ClickableComponent):
    """Extends ClickableComponent; provides rendering a pause button and a way to check if the pause button is clicked"""

    color = (250, 250, 250)

    pause_font = pygame.font.Font('freesansbold.ttf', 53)
    normal_font = pygame.font.Font('freesansbold.ttf', 15)

    def render(self):
        """ summary: renders two rectangles giving the 'classic' pause button look
            params: None
            returns: None
        """

        # A pause button is made up of two rectangles of equal length and height
        rectangle_length = VelocityCalculator.give_measurement(screen_length, .7)

        pygame.draw.rect(game_window.get_window(), (self.color), (self.x_coordinate,
                         self.y_coordinate, rectangle_length, self.height))
        # Buffer is the space between the two rectangles making up the pause button
        # then x_coordinate is for the 2nd rectangle that makes up the pause button
        buffer = VelocityCalculator.give_measurement(screen_length, 1.3)
        x_coordinate = self.x_coordinate + rectangle_length + buffer

        pygame.draw.rect(game_window.get_window(), (self.color), (x_coordinate,
                         self.y_coordinate, rectangle_length, self.height))

    def __init__(self):
        """ summary: initializes the pause button's dimensions and the event that checks if the  pause button was clicked
            params: None
            returns: None
        """

        self.number_set_dimensions(VelocityCalculator.give_measurement(screen_length, 96),
                                   VelocityCalculator.give_measurement(screen_height, 1),
                                   VelocityCalculator.give_measurement(screen_length, 2.7),
                                   VelocityCalculator.give_measurement(screen_height, 5))
        super().__init__()

