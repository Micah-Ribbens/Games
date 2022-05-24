import unittest

from base_pong.quadratic_equations import QuadraticEquation, PhysicsEquation
from base_pong.equations import Point


class GravityPongTests(unittest.TestCase):
    def test_quadratic_equation(self):
        equation = QuadraticEquation()
        equation.points_set_variables(Point(.2, 300), Point(0, 500))
        wanted_outputs = [300, 500, 500]
        gotten_outputs = [
            equation.get_number(.2),
            equation.get_number(.4),
            equation.get_number(0)
        ]
        for x in range(len(wanted_outputs)):
            self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                             f"Test Case number {x + 1} out of {len(wanted_outputs)} Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_get_velocity_using_displacement(self):
        equation = PhysicsEquation()
        equation.set_all_variables(250, .4, -250, 0)

        wanted_outputs = [
            0,
            equation.initial_velocity
        ]

        gotten_outputs = [
            equation.get_velocity_using_displacement(250),
            equation.get_velocity_using_displacement(0)
        ]

        for x in range(len(wanted_outputs)):
            self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                             f"Test Case number {x} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_get_displacement(self):
        equation = PhysicsEquation()
        equation.set_all_variables(250, .2, -250, 0)

        wanted_outputs = [
            .2
        ]

        gotten_outputs = [
            equation.get_time_to_vertex()
        ]

        for x in range(len(wanted_outputs)):
            self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                             f"Test Case number {x} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")


if __name__ == '__main__':
    unittest.main()
