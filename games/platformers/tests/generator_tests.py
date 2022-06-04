import cProfile

import pygame.display

from base.engines import CollisionsFinder
from base.path import *
from base.utility_classes import HistoryKeeper
from base.important_variables import *
import time
from base.velocity_calculator import VelocityCalculator
from games.platformers.base.platform import Platform
from games.platformers.tests.generator_test_screen import GeneratorTestScreen
from gui_components.navigation_screen import NavigationScreen
from gui_components.screen import Screen


class GeneratorSelectorScreen(NavigationScreen):
    """The screen for testing the generator; this screen is for navigating between the different screens"""

    sub_screens = [GeneratorTestScreen(1, 20, 100, [Platform(100, 400, 300, 100, True)], [Platform(700, 200, 300, 100, True)], [Platform(700, 550, 300, 100, True)], []),
                    GeneratorTestScreen(2, 20, 100, [Platform(400, 550, 300, 100, True)], [Platform(700, 350, 300, 100, True)], [Platform(700, 600, 300, 100, True)], [])] + [Screen()] * 98

    def __init__(self):
        """Initializes the object"""

        super().__init__(self.sub_screens, ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '100'])


game_window.add_screen(GeneratorSelectorScreen())
total_frames = 0
total_time = 0

while True:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f"Average Frames {total_frames / total_time} Total Frames {total_frames} Total Time {total_time}")
            pygame.quit()

    game_window.run()

    CollisionsFinder.objects_to_data = {}
    function_runner.run()
    changer.run_changes()
    HistoryKeeper.last_time = VelocityCalculator.time
    VelocityCalculator.time = time.time() - start_time
    total_frames += 1
    total_time += VelocityCalculator.time

