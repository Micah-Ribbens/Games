import pygame

from base.engines import CollisionsFinder
from base.important_variables import screen_height
from base.velocity_calculator import VelocityCalculator
from games.platformers.base.gravity_engine import GravityEngine
from games.platformers.base.platform import Platform
from games.platformers.base.player import Player
from gui_components.screen import Screen


class PlatformerScreen(Screen):
    """A basic platformer game"""

    player = Player(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_f)
    gravity_engine = None
    platform = Platform()
    components = [platform, player]
    time_elapsed = 0

    def __init__(self):
        """Initializes the object"""

        self.gravity_engine = GravityEngine([self.player], .5, screen_height/2)
        self.player.jumping_equation.acceleration = self.gravity_engine.physics_paths[0].acceleration
        self.player.y_coordinate = self.platform.y_coordinate - self.player.height
        self.player.base_y_coordinate = self.player.y_coordinate
        self.player.set_y_coordinate(self.player.base_y_coordinate)

    def run(self):
        """Runs all the code necessary in order for the platformer to work"""

        self.player.run()
        self.gravity_engine.run()
        player_is_on_platform = CollisionsFinder.is_collision(self.player, self.platform)

        if not player_is_on_platform:
            self.time_elapsed += VelocityCalculator.time

        if player_is_on_platform:
            self.player.y_coordinate = self.platform.y_coordinate - self.player.height

        self.player.set_is_on_platform(player_is_on_platform)

        if self.player.y_coordinate >= screen_height:
            self.reset_game()

    def reset_game(self):
        """Resets the game after the player's death"""

        self.player.reset()
        self.gravity_engine.reset()