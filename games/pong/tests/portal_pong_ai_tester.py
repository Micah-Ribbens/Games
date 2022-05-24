import time

import pygame

from base_pong.ball import Ball
from base_pong.important_variables import game_window
from base_pong.players import Player
from base_pong.quadratic_equations import PhysicsEquation
from base_pong.utility_classes import HistoryKeeper
from base_pong.velocity_calculator import VelocityCalculator
from logic.file_reader import FileReader
from pong_types.gravity_pong import GravityPong
from pong_types.portal_pong import PortalPong
from tests.AI_GUI import TestCase, AI_GUI


class TestData:
    """Stores all the data necessary for testing Gravity Pong AI"""

    end_x_coordinate = 0
    ball_x_coordinate = 0
    ball_y_coordinate = 0
    ball_forwards_velocity = 0
    actual_y_coordinate = 0 # The y_coordinate the ball ended on
    ball_upwards_velocity = 0
    portal_path_times = []
    portal_timed_events = []
    ball_is_moving_down = False


    def __init__(self, end_x_coordinate, ball_x_coordinate, ball_y_coordinate, ball_forwards_velocity,
                 ball_upwards_velocity, actual_y_coordinate, portal_path_times, portal_timed_events, ball_is_moving_down):
        """Initializes the object"""

        self.end_x_coordinate, self.ball_x_coordinate = end_x_coordinate, ball_x_coordinate
        self.ball_y_coordinate, self.ball_forwards_velocity = ball_y_coordinate, ball_forwards_velocity
        self.ball_upwards_velocity, self.actual_y_coordinate = ball_upwards_velocity, actual_y_coordinate
        self.portal_path_times, self.portal_timed_events = portal_path_times, portal_timed_events
        self.ball_is_moving_down = ball_is_moving_down


class GravityPongAITester:
    """Tests the AI for gravity pong"""

    all_data = []
    tests = []
    cases = []

    def get_cases(self):
        """returns: List of Case; all the data necessary for the GUI to display stuff; gotten from running the tests"""

        self.all_data = []
        fr = FileReader("C:\\Users\\mdrib\\Downloads\\Games\\Pong\\portal_pong_data.txt")

        for x in range(fr.get_int("number_of_tests")):
            s = f"test_number{x + 1}."

            self.tests.append(TestData(fr.get_double(f"{s}end_x_coordinate"), fr.get_double(f"{s}ball_x_coordinate"),
                                       fr.get_double(f"{s}ball_y_coordinate"), fr.get_double(f"{s}ball_forwards_velocity"),
                                       fr.get_double(f"{s}ball_upwards_velocity"), fr.get_double(f"{s}actual_y_coordinate"),
                                       fr.get_number_list(f"{s}path_times"), fr.get_number_list(f"{s}portal_timed_events"),
                                       fr.get_boolean(f"{s}ball_is_moving_down")))

        for x in range(len(self.tests)):
            self.run_test(x + 1)

        return self.cases

    def run_test(self, test_number):
        """returns: Case; the data gotten from running the tests; data is used for the GUI"""

        index = test_number - 1
        ball = Ball()
        portal_pong = PortalPong(Player(), Player(), ball)

        test_data: TestData = self.tests[index]

        ball.x_coordinate = test_data.ball_x_coordinate
        ball.y_coordinate = test_data.ball_y_coordinate
        ball.forwards_velocity = test_data.ball_forwards_velocity
        ball.upwards_velocity = test_data.ball_upwards_velocity
        ball.is_moving_down = test_data.ball_is_moving_down


        for x in range(len(test_data.portal_timed_events)):
            portal_pong.portals[x].can_be_enabled_event.current_time = test_data.portal_timed_events[x]

        for x in range(len(test_data.portal_path_times)):
            portal_pong.portal_paths[x].total_time = test_data.portal_path_times[x]

        # for x in range(test):

        predicted_y_coordinate, time = portal_pong.get_ai_data(test_data.end_x_coordinate - ball.length)
        self.cases.append(TestCase(predicted_y_coordinate, test_data.actual_y_coordinate, test_data.end_x_coordinate))

screen = AI_GUI(GravityPongAITester().get_cases(), 10)
game_window.add_screen(screen)
while True:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    game_window.run()

    HistoryKeeper.last_time = VelocityCalculator.time
    VelocityCalculator.time = time.time() - start_time
