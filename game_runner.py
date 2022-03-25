import cProfile

import pygame.display

from base.engines import CollisionsFinder
from base.path import *
from base.utility_classes import HistoryKeeper
from base.important_variables import *
import time
from base.velocity_calculator import VelocityCalculator
from gui.main_screen import MainScreen
import re

from minigames.card_games.word_finder import WordFinder

game_window.add_screen(MainScreen())

def run():
    while True:
        start_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        game_window.run()

        CollisionsFinder.objects_to_data = {}
        function_runner.run()
        changer.run_changes()
        HistoryKeeper.last_time = VelocityCalculator.time
        VelocityCalculator.time = time.time() - start_time

cProfile.run("run()", None, "cumtime")
