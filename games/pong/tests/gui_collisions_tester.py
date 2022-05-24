import unittest
import time

import pygame

from base_pong.drawable_objects import GameObject, Ellipse
from base_pong.engine_utility_classes import CollisionsUtilityFunctions
from base_pong.engines import CollisionsFinder
from base_pong.equations import Point, LineSegment
from base_pong.important_variables import game_window
from base_pong.path import Path, ObjectPath
from base_pong.utility_classes import HistoryKeeper
from base_pong.utility_functions import solve_quadratic
from base_pong.velocity_calculator import VelocityCalculator
from tests.collisions_tester import FailedCase, CollisionsTester
from gui_components.graph import Graph
from base_pong.colors import *


def get_path(point1, point2, height):
    path = Path(point1)
    path.add_point(point2, height)
    return path


class CollisionsFinderTests:

    def test_is_moving_collision_ellipse(self):
        moving_object_start = GameObject(30, 30, 10, 10)
        moving_object_end = GameObject(0, 0, 10, 10)
        non_moving_object = GameObject(0, 20, 20, 20)

        self.simulate_game([moving_object_start], [non_moving_object], [moving_object_end], [non_moving_object])

        gotten_outputs = [
            CollisionsFinder.is_moving_collision(moving_object_end, non_moving_object),
            CollisionsFinder.is_moving_collision(moving_object_end, self.turn_into_ellipse(non_moving_object)),
        ]
        wanted_outputs = [
            True,
            True
        ]
        for x in range(len(gotten_outputs)):
            if gotten_outputs[x] != wanted_outputs[x]:
                self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                                 f"Test Case number {x + 1} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_line_collision(self):
        line1 = LineSegment(Point(10, 20), Point(10, 40))
        line2 = LineSegment(Point(20, 40), Point(0, 10))

        gotten_outputs = [CollisionsUtilityFunctions.is_line_collision(line1, line2)]
        wanted_outputs = [True]
        for x in range(len(gotten_outputs)):
            if gotten_outputs[x] != wanted_outputs[x]:
                self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                                 f"Test Case number {x + 1} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_is_line_ellipse_collision(self):
        line = LineSegment(Point(-2, 0), Point(2, 1))
        ellipse = Ellipse(-1, -1, 2, 2)
        gotten_outputs = [CollisionsFinder.is_line_ellipse_collision(line, ellipse)]
        wanted_outputs = [True]
        for x in range(len(gotten_outputs)):
            if gotten_outputs[x] != wanted_outputs[x]:
                self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                                 f"Test Case number {x + 1} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_solve_quadratic(self):
        gotten_outputs = [
            solve_quadratic(1, -30, 125),
            solve_quadratic(200, -6000, 40000)
        ]

        wanted_outputs = [
            [5, 25],
            [10, 20]
        ]
        for x in range(len(gotten_outputs)):
            if gotten_outputs[x] != wanted_outputs[x]:
                self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                                 f"Test Case number {x + 1} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_is_collision(self):
        # Stores whether the cases have passed or not
        cases = []
        # STATIONARY TESTS
        # Case 1; True
        stationary_object = GameObject(20, 20, 30, 20)
        prev_moving_object = GameObject(10, 25, 5, 5)
        current_moving_object = GameObject(30, 25, 5, 5)
        cases += self.get_failed_cases(stationary_object, prev_moving_object, stationary_object, current_moving_object, True, 1)

        # Case 2; True
        prev_moving_object = GameObject(50, 25, 5, 5)
        current_moving_object = GameObject(33, 30, 5, 5)
        cases += self.get_failed_cases(stationary_object, prev_moving_object, stationary_object, current_moving_object, True, 2)

        # Case 3; False
        stationary_object = GameObject(10, 60, 10, 10)
        prev_moving_object = GameObject(10, 40, 10, 10)
        current_moving_object = GameObject(40, 70, 10, 10)
        cases += self.get_failed_cases(stationary_object, prev_moving_object, stationary_object, current_moving_object, False, 3)

        # Case 4; True (Up and Down)
        stationary_object = GameObject(10, 60, 10, 10)
        prev_moving_object = GameObject(10, 70, 10, 10)
        current_moving_object = GameObject(10, 49, 10, 10)
        cases += self.get_failed_cases(stationary_object, prev_moving_object, stationary_object, current_moving_object, True, 4)

        # Case 5; True (Up and Down)
        stationary_object = GameObject(10, 50, 10, 10)
        prev_moving_object = GameObject(10, 40, 10, 10)
        current_moving_object = GameObject(20, 53, 10, 10)
        cases += self.get_failed_cases(stationary_object, prev_moving_object, stationary_object, current_moving_object, True, 5)

        # PATH TESTS
        # Case 1; one object envelopes the other
        prev_object1 = GameObject(40, 30, 10, 10)
        current_object1 = GameObject(50, 20, 10, 10)

        prev_object2 = GameObject(30, 10, 40, 30)
        current_object2 = GameObject(60, 10, 40, 30)
        cases += self.get_failed_cases(prev_object1, prev_object2, current_object1, current_object2, True, 1)

        # Case 2; both touching, but they move away from each other
        prev_object1 = GameObject(40, 30, 10, 10)
        current_object1 = GameObject(50, 20, 10, 10)

        prev_object2 = GameObject(30, 10, 40, 10)
        current_object2 = GameObject(20, 10, 40, 10)
        cases += self.get_failed_cases(prev_object1, prev_object2, current_object1, current_object2, False, 2)

        # Case 3; both touching, but object1 moves into object2
        prev_object1 = GameObject(30, 10, 10, 10)
        current_object1 = GameObject(40, 20, 10, 10)

        prev_object2 = GameObject(40, 10, 40, 10)
        current_object2 = GameObject(45, 10, 40, 10)
        cases += self.get_failed_cases(prev_object1, prev_object2, current_object1, current_object2, True, 3)

        # Case 4; From the game
        prev_object1 = GameObject(233, 429, 25, 25)
        current_object1 = GameObject(241, 422, 25, 25)

        prev_object2 = GameObject(209, 350, 150, 24)
        current_object2 = GameObject(227, 350, 150, 24)
        cases += self.get_failed_cases(prev_object1, prev_object2, current_object1, current_object2, True, 4)

        return cases

        # for x in range(len(cases) // 2):
        #     if not cases[x * 2] or not cases[x * 2 + 1]:
        #         failed_cases += f"{x + 1} --> "
        #
        #         failed_cases += "Rectangle, " if not cases[x * 2] else ""
        #         failed_cases += "Ellipse " if not cases[x * 2 + 1] else ""

        # self.assertEqual(True, failed_cases == "", f"These are the failed cases; {failed_cases} ")

    def get_failed_cases(self, prev_object1, prev_object2, object1, object2, want, test_case_number):
        """returns: List of boolean; [rectangle collision worked, elliptical collision worked]"""

        failed_cases = []
        object1_has_moved = prev_object1.x_coordinate != object1.x_coordinate or prev_object1.y_coordinate != object1.y_coordinate
        object2_has_moved = prev_object2.x_coordinate != object2.x_coordinate or prev_object2.y_coordinate != object2.y_coordinate
        case_type = "Path" if object1_has_moved and object2_has_moved else "Moving"
        # Case 1; rectangle
        self.simulate_game([prev_object1], [prev_object2], [object1], [object2])

        got = CollisionsFinder.is_collision(object1, object2)
        if got != want:
            CollisionsFinder.is_collision(object1, object2)
            failed_cases.append(FailedCase(want, got, case_type, test_case_number,
                                           ObjectPath(prev_object1, object1), ObjectPath(prev_object2, object2)))

        # Case 2; Ellipse
        got = CollisionsFinder.is_collision(self.turn_into_ellipse(object1), self.turn_into_ellipse(object2))
        if got != want:
            print("CASE FAILED ELLIPSE", f"{case_type}: {test_case_number}")
            failed_cases.append(FailedCase(want, got, case_type, test_case_number,
                                           ObjectPath(prev_object1, self.turn_into_ellipse(object1)),
                                           ObjectPath(prev_object2, self.turn_into_ellipse(object2))))
        return failed_cases

    def turn_into_ellipse(self, rectangle):
        ellipse = Ellipse(rectangle.x_coordinate, rectangle.y_coordinate, rectangle.height, rectangle.length)
        ellipse.name = rectangle.name
        return ellipse

    def simulate_game(self, prev_object1s, prev_object2s, object1s, object2s):
        CollisionsFinder.objects_to_data = {}
        HistoryKeeper.reset()
        VelocityCalculator.time = 1
        HistoryKeeper.last_time = 1

        for x in range(len(prev_object1s)):
            prev_object1 = prev_object1s[x]
            prev_object1.name = id(prev_object1)
            object1s[x].name = prev_object1.name
            HistoryKeeper.add(prev_object1, prev_object1.name, True)

        for x in range(len(prev_object2s)):
            prev_object2 = prev_object2s[x]
            prev_object2.name = id(prev_object2)
            object2s[x].name = prev_object2.name
            HistoryKeeper.add(prev_object2, prev_object2.name, True)

        VelocityCalculator.time = 2



# if __name__ == '__main__':
#     unittest.main()
# graph = Graph([LineSegment(Point(30, 50), Point(10, 45)), LineSegment(Point(90, 30), Point(25, 56))], [purple, red])
# graph.percentage_set_dimensions(10, 10, 20, 20)
# game_window.add(graph)
screen = CollisionsTester(CollisionsFinderTests().test_is_collision())
game_window.add_screen(screen)
while True:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    game_window.run()

    CollisionsFinder.objects_to_data = {}
    HistoryKeeper.last_time = VelocityCalculator.time
    VelocityCalculator.time = time.time() - start_time