from gui_components.window import Window
from base.function_runner import FunctionRunner
from utillities.changer import Changer
import pygame

background_color = (70, 70, 70)
screen_length = 1280
screen_height = 650
game_window = Window(screen_length, screen_height, "Pong Reloaded", background_color)
function_runner = FunctionRunner()
changer = Changer()
pygame.init()
