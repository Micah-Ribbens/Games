from gui_components.screen import Screen
from gui_components.button import Button
from gui_components.text_box import TextBox
from base.colors import *
from base.important_variables import *
from base.velocity_calculator import VelocityCalculator
from gui_components.grid import Grid
from base.dimensions import Dimensions


class PauseScreen(Screen):
    """The screen that is displayed when the game is paused"""

    continue_game_button = Button("Continue Game", 30, white, green)
    go_to_start_screen_button = Button(
        "Go Back to Start Screen", 30, white, green)
    game_paused_text_box = TextBox(
        "Game Paused", 40, False, white, background_color)
    components = [continue_game_button, go_to_start_screen_button, game_paused_text_box]

    def __init__(self):
        """ summary: initializes the object
            params: None
            returns: None
        """

        PauseScreen.game_paused_text_box.percentage_set_dimensions(0, 0, 100, 40)
        buffer = VelocityCalculator.give_measurement(screen_height, 5)

        x_coordinate = 0
        length = screen_length

        height_used_up = buffer + PauseScreen.game_paused_text_box.height
        y_coordinate = height_used_up
        height = screen_height - height_used_up

        grid = Grid(Dimensions(x_coordinate, y_coordinate,
                    length, height), 2, None, True)
        grid.turn_into_grid([PauseScreen.go_to_start_screen_button,
                            PauseScreen.continue_game_button], None, None)

