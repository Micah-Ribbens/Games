import pygame
from gui_components.window import Window
from base.function_runner import FunctionRunner
from utillities.changer import Changer

screen_length = 800
screen_height = 500
background_color = (70, 70, 70)
game_window = Window(screen_length, screen_height, "Pong Reloaded", background_color)
function_runner = FunctionRunner()
changer = Changer()

