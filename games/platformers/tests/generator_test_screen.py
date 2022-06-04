import pygame

from base.dimensions import Dimensions
from base.events import Event
from base.utility_classes import HistoryKeeper
from base.utility_functions import *
from games.platformers.base.gravity_engine import GravityEngine
from games.platformers.base.player import Player
from games.platformers.platformer_screen import PlatformerScreen
from base.important_variables import *
from gui_components.grid import Grid
from gui_components.text_box import TextBox
from base.colors import *


class GeneratorTestScreen(PlatformerScreen):
    """A screen that is used for testing the generator"""

    screen_number_field = None
    platform_type_field = None
    generation_difficulty_field = None
    main_platform_number_field = None
    main_platforms = []
    highest_platforms = []
    lowest_platforms = []
    player_end_locations = []
    current_index = 0
    is_hard_platform = True
    hud = None

    increase_main_platform_number_event = None
    decrease_main_platform_number_event = None
    change_is_hard_platform_event = None

    def __init__(self, screen_number, total_screens, generation_difficulty, main_platforms, highest_platforms, lowest_platforms, player_end_locations):
        """Initializes the object"""

        self.players = [Player(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_f, self.is_gone)]
        self.gravity_engine = GravityEngine(self.players, self.players[0].jumping_path.acceleration)

        self.highest_platforms, self.lowest_platforms = highest_platforms, lowest_platforms
        self.main_platforms, self.player_end_locations = main_platforms, player_end_locations

        # Have to do this here, so I can put the player on the platform
        other_platform_list = self.highest_platforms if self.is_hard_platform else self.lowest_platforms
        self.platforms = [self.main_platforms[self.current_index], other_platform_list[self.current_index]]

        for player in self.players:
            player.gravity_engine = self.gravity_engine
            player.x_coordinate = self.platforms[0].x_coordinate + 10
            player.base_y_coordinate = self.platforms[0].y_coordinate - player.height
            player.set_y_coordinate(player.base_y_coordinate)

        self.screen_number_field = TextBox(f"Screen Number {screen_number} of {total_screens}", 20, False, purple, white)
        self.platform_type_field = TextBox("", 20, False, medium_green, white)
        self.generation_difficulty_field = TextBox(f"Generation Difficulty: {generation_difficulty}", 20, False, black, white)
        self.main_platform_number_field = TextBox("", 20, False, blue, white)

        self.increase_main_platform_number_event = Event()
        self.decrease_main_platform_number_event = Event()
        self.change_is_hard_platform_event = Event()

        self.hud = [self.screen_number_field, self.platform_type_field, self.generation_difficulty_field, self.main_platform_number_field]
        grid = Grid(Dimensions(0, 0, screen_length, screen_height * .1), None, 1, True)
        grid.turn_into_grid(self.hud, None, None)

    def run(self):
        """Runs all that is necessary to have a generator test screen"""

        other_platform_list = self.highest_platforms if self.is_hard_platform else self.lowest_platforms
        self.platforms = [self.main_platforms[self.current_index], other_platform_list[self.current_index]]
        # Changeable keys
        self.increase_main_platform_number_event.run(key_is_hit(pygame.K_UP))
        self.decrease_main_platform_number_event.run(key_is_hit(pygame.K_DOWN))
        self.change_is_hard_platform_event.run(key_is_hit(pygame.K_SPACE))

        self.main_platform_number_field.text = f"Main Platform #{self.current_index + 1}"
        self.platform_type_field.text = "Showing Hard Platform" if self.is_hard_platform else "Is Showing Easy Platform"

        if self.decrease_main_platform_number_event.is_click():
            self.current_index = get_prev_index(self.current_index, len(self.main_platforms) - 1)

        if self.increase_main_platform_number_event.is_click():
            self.current_index = get_next_index(self.current_index, len(self.main_platforms) - 1)

        if self.change_is_hard_platform_event.is_click():
            self.is_hard_platform = not self.is_hard_platform

        # If the platforms were changed then the game should be reset
        if self.decrease_main_platform_number_event.is_click() or self.increase_main_platform_number_event.is_click():
            self.reset_game()

        super().run()

    def get_components(self):
        """returns: Component[]; all the components that should be ran and rendered"""

        return self.hud + self.platforms + self.players

    def reset_game(self):
        """Resets the game after the player's death"""

        for player in self.players:
            player.x_coordinate = self.platforms[0].x_coordinate
            player.base_y_coordinate = self.platforms[0].y_coordinate - player.height - 10
            player.set_y_coordinate(player.base_y_coordinate)

        self.gravity_engine.reset()
        HistoryKeeper.last_objects = {}
        self.frames = 0

    def setup(self):
        self.reset_game()

