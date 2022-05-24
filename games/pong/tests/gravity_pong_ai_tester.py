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
from tests.AI_GUI import TestCase, AI_GUI


class TestData:
    """Stores all the data necessary for testing Gravity Pong AI"""

    end_x_coordinate = 0
    ball_x_coordinate = 0
    ball_y_coordinate = 0
    ball_forwards_velocity = 0
    time_in_air = 0
    actual_y_coordinate = 0 # The y_coordinate the ball ended on
    bottom_to_top_physics_equation = None
    current_physics_equation = None
    needed_vertex_increase = None

    def __init__(self, end_x_coordinate, ball_x_coordinate, ball_y_coordinate, ball_forwards_velocity, time_in_air,
                 actual_y_coordinate, bottom_to_top_physics_equation, current_physics_equation, needed_vertex_increase):
        """Initializes the object"""

        self.end_x_coordinate, self.ball_x_coordinate = end_x_coordinate, ball_x_coordinate
        self.ball_y_coordinate, self.ball_forwards_velocity = ball_y_coordinate, ball_forwards_velocity
        self.time_in_air, self.actual_y_coordinate = time_in_air, actual_y_coordinate
        self.bottom_to_top_physics_equation, self.current_physics_equation = bottom_to_top_physics_equation, current_physics_equation
        self.needed_vertex_increase = needed_vertex_increase


class GravityPongAITester:
    """Tests the AI for gravity pong"""

    all_data = []
    tests = []
    cases = []

    def get_cases(self):
        """returns: List of Case; all the data necessary for the GUI to display stuff; gotten from running the tests"""

        self.all_data = []
        fr = FileReader("C:\\Users\\mdrib\\Downloads\\Games\\Pong\\data.txt")

        for x in range(fr.get_int("number_of_tests")):
            s = f"test_number{x + 1}."
            bottom_to_top_physics_equation = PhysicsEquation()
            acceleration, initial_velocity, initial_distance = fr.get_number_list(f"{s}bottom_to_top_physics_equation")
            bottom_to_top_physics_equation.set_variables(acceleration=acceleration, initial_velocity=initial_velocity, initial_distance=initial_distance)

            current_physics_equation = PhysicsEquation()
            acceleration, initial_velocity, initial_distance = fr.get_number_list(f"{s}current_physics_equation")
            current_physics_equation.set_variables(acceleration=acceleration, initial_velocity=initial_velocity, initial_distance=initial_distance)

            self.tests.append(TestData(fr.get_double(f"{s}end_x_coordinate"), fr.get_double(f"{s}ball_x_coordinate"),
                                       fr.get_double(f"{s}ball_y_coordinate"), fr.get_double(f"{s}ball_forward_velocity"),
                                       fr.get_double(f"{s}time"), fr.get_double(f"{s}actual_y_coordinate"),
                                       bottom_to_top_physics_equation, current_physics_equation, fr.get_double(f"{s}needed_vertex_increase")))

        for x in range(len(self.tests)):
            self.run_test(x + 1)

        return self.cases

    def run_test(self, test_number):
        """returns: Case; the data gotten from running the tests; data is used for the GUI"""

        index = test_number - 1
        ball = Ball()
        gravity_pong = GravityPong(Player(), Player(), ball)

        test_data: TestData = self.tests[index]
        ball.x_coordinate = test_data.ball_x_coordinate
        ball.y_coordinate = test_data.ball_y_coordinate
        gravity_pong.time = test_data.time_in_air
        ball.forwards_velocity = test_data.ball_forwards_velocity
        gravity_pong.bottom_to_top_physics_equation = test_data.bottom_to_top_physics_equation
        gravity_pong.physics_equation = test_data.current_physics_equation
        gravity_pong.needed_vertex_increase = test_data.needed_vertex_increase

        predicted_y_coordinate = gravity_pong.get_ball_path_from(test_data.ball_y_coordinate, test_data.ball_x_coordinate,
                                                                 test_data.end_x_coordinate, True)
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
