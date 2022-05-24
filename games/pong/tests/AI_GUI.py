import pygame

from base_pong.ball import Ball
from base_pong.dimensions import Dimensions
from base_pong.important_variables import background_color, screen_length, screen_height
from base_pong.utility_functions import percentages_to_numbers, get_next_index, get_prev_index
from gui_components.grid import Grid
from gui_components.screen import Screen
from gui_components.text_box import TextBox
from base_pong.colors import *


class TestCase:
    """Stores all the data for running a test"""

    predicted_y_coordinate = 0
    actual_y_coordinate = 0
    end_x_coordinate = 0

    def __init__(self, predicted_y_coordinate, actual_y_coordinate, end_x_coordinate):
        """Initializes the object"""

        self.predicted_y_coordinate, self.actual_y_coordinate = predicted_y_coordinate, actual_y_coordinate
        self.end_x_coordinate = end_x_coordinate


class AI_GUI(Screen):
    """GUI for testing AI"""

    cases = []
    deviation_acceptable = 0
    all_screens = []
    deviating_screens = []
    current_screens = all_screens
    current_screen_index = 0
    right_clicked_last_cycle = False
    left_clicked_last_cycle = False
    h_clicked_last_cycle = False

    def __init__(self, cases, deviation_acceptable):
        """Initializes the object"""

        self.cases, self.deviation_acceptable = cases, deviation_acceptable

        for x in range(len(self.cases)):
            self.add_screen(x + 1)

    def add_screen(self, case_number):
        """Adds the screen that is associated with the case_number"""

        case = self.cases[case_number - 1]
        deviation = abs(case.actual_y_coordinate - case.predicted_y_coordinate)

        has_predicted_wrongly = deviation > self.deviation_acceptable

        # General Information for the screen
        screen_indicator_field = TextBox(f"Screen Number {case_number}/{len(self.cases)}", 15, False, brown, white)
        deviation_field = TextBox(f"Deviation: {deviation}", 15, False, dark_green, white)
        has_predicted_wrongly_field = TextBox(f"Has Predicted Wrongly: {has_predicted_wrongly}", 15, False, orange, white)
        actual_y_coordinate_field = TextBox(f"Actual Y Coordinate: {case.actual_y_coordinate}", 15, False, black, white)
        predicted_y_coordinate_field = TextBox(f"Predicted Y Coordinate: {case.predicted_y_coordinate}", 15, False, purple, white)

        information_components = [screen_indicator_field, actual_y_coordinate_field, predicted_y_coordinate_field,
                                  deviation_field, has_predicted_wrongly_field]

        x_coordinate, y_coordinate, length, height = percentages_to_numbers(0, 0, 100, 20, screen_length, screen_height)
        grid = Grid(Dimensions(x_coordinate, y_coordinate, length, height), None, 2, True)
        grid.turn_into_grid(information_components, None, None)

        # Showing the balls
        predicted_ball = Ball()
        predicted_ball.x_coordinate = case.end_x_coordinate
        predicted_ball.y_coordinate = case.predicted_y_coordinate
        predicted_ball.color = blue
        predicted_ball.is_outline = True

        actual_ball = Ball()
        actual_ball.x_coordinate = case.end_x_coordinate
        actual_ball.y_coordinate = case.actual_y_coordinate
        actual_ball.color = red
        actual_ball.is_outline = True

        screen = Screen()
        screen.components = information_components + [actual_ball, predicted_ball]
        self.all_screens.append(screen)

    def get_components(self):
        """returns: List of Component; the components that should be rendered"""

        return self.current_screens[self.current_screen_index].get_components()

    def run(self):
        """Runs all the code necessary for this screen to work properly"""

        controls = pygame.key.get_pressed()

        if controls[pygame.K_RIGHT] and not self.right_clicked_last_cycle:
            self.current_screen_index = get_next_index(self.current_screen_index, len(self.current_screens) - 1)

        if controls[pygame.K_LEFT] and not self.left_clicked_last_cycle:
            self.current_screen_index = get_prev_index(self.current_screen_index, len(self.current_screens) - 1)

        if controls[pygame.K_h] and not self.h_clicked_last_cycle:
            self.current_screens = self.deviating_screens if self.current_screens == self.deviating_screens else self.all_screens

        self.right_clicked_last_cycle = controls[pygame.K_RIGHT]
        self.left_clicked_last_cycle = controls[pygame.K_LEFT]
        self.h_clicked_last_cycle = controls[pygame.K_h]




