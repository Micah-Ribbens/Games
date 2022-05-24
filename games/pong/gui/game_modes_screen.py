from base.dimensions import Dimensions
from base.important_variables import screen_length, screen_height
from base.utility_functions import percentage_to_number
from gui_components.drop_down_menu import DropDownMenu
from gui_components.grid import Grid
from gui_components.sub_screen import SubScreen
from base.colors import *
from games.pong.pong_types.game_mode_selector import GameModeSelector


class GameModesScreen(SubScreen):
    """The screen that allows the user to select the game mode"""

    pong_type_menu = DropDownMenu(
        "Pong Types", GameModeSelector.all_pong_types, white, blue, 20, GameModeSelector.all_pong_types.index(GameModeSelector.pong_type))
    player_menu = DropDownMenu(
        "Number Of Players", GameModeSelector.all_player_options, white, blue, 20, GameModeSelector.all_player_options.index(GameModeSelector.number_of_players))
    game_mode_menu = DropDownMenu(
        "Game Modes", GameModeSelector.all_game_modes, white, blue, 20, GameModeSelector.all_game_modes.index(GameModeSelector.game_mode))
    ai_difficulty_level_menu = DropDownMenu("AI Difficulty", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], white, blue, 20, 4)
    components = [game_mode_menu, player_menu, pong_type_menu, ai_difficulty_level_menu]
    length_used_up = 0
    height_used_up = 0
    name = "Game Modes"
    most_items = 0

    def __init__(self, length_used_up, height_used_up):
        """ summary: initializes the object

            params:
                length_used_up: int; the amount of length that the main screen takes up
                height_used_up: int; the amount of height the main screen takes up

            returns: None
        """

        GameModeSelector.pong_type = self.pong_type_menu.selected_item
        GameModeSelector.game_mode = self.game_mode_menu.selected_item
        self.height_used_up = height_used_up

        for menu in self.components:
            if len(menu.items) > self.most_items:
                self.most_items = len(menu.items)

    def run(self):
        """ summary: runs all the necessary logic in order for the game modes screen to work
            params: None
            returns: None
        """

        GameModeSelector.game_mode = self.game_mode_menu.get_selected_item()

        if self.game_mode_menu.get_selected_item() == "Pick Pong Type":
            GameModeSelector.pong_type = self.pong_type_menu.get_selected_item()

        if self.player_menu.get_selected_item() == "Single Player":
            GameModeSelector.ai_difficulty = int(self.ai_difficulty_level_menu.get_selected_item())
        
        items = [self.game_mode_menu, self.player_menu]

        # The user gets to choose between certain game modes or choose a specific Pong Type like "Gravity Pong"
        # The Pong Types should only be displayed if they want to pick a specific Pong Type
        items += [self.pong_type_menu] if self.game_mode_menu.get_selected_item() == "Pick Pong Type" else []

        is_single_player = self.player_menu.get_selected_item() == "Single Player"
        items += [self.ai_difficulty_level_menu] if is_single_player else []

        # Only the components that are put into the grid should be rendered
        for component in self.components:
            if not items.__contains__(component):
                component.is_visible = False

            else:
                component.is_visible = True

            component.set_item_height(self.most_items)

        grid = Grid(Dimensions(0, self.height_used_up, screen_length, screen_height - self.height_used_up), 2, None, True)
        grid.turn_into_grid(items, None, None)

        GameModeSelector.number_of_players = "Single Player" if is_single_player else "2 Player"
