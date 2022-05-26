from base.utility_functions import get_random_item
from games.pong.pong_types.gravity_pong import GravityPong
from games.pong.pong_types.middle_paddle_pong import MiddlePaddlePong
from games.pong.pong_types.normal_pong import NormalPong
from games.pong.pong_types.portal_pong import PortalPong
from games.pong.pong_types.shatter_pong import ShatterPong
from games.pong.pong_types.split_pong import SplitPong
from games.pong.pong_types.omnidirection_pong import OmnidirectionalPong


class GameModeSelector:
    """The class that holds the game modes and pong types"""

    # If a game mode isn't selected from the gui, then the game mode will be Random
    game_mode = "Pick Pong Type"
    # If a pong_type isn't selected from the gui, then the game mode will be Normal Pong
    pong_type = "Omnidirectional Pong"
    number_of_players = "Single Player"

    all_game_modes = ["Chaos", "Civilized",
                      "Unique Twist", "Random", "Pick Pong Type"]
    all_player_options = ["Single Player", "2 Player"]
    all_pong_types = ["Gravity Pong", "Middle Paddle Pong",
                      "Normal Pong", "Portal Pong", "Shatter Pong", "Split Pong", "Omnidirectional Pong"]
    ai_difficulty = 0

    def get_pong_type_class(pong_type):
        """ summary: turns the pong type into the class the string represents

            params:
                pong_type: String; the name of the pong type

            returns: PongType; the class that the string pong_type represents
        """

        # Each pong type has its own class
        pong_type_to_class = {
            "Gravity Pong": GravityPong,
            "Middle Paddle Pong": MiddlePaddlePong,
            "Normal Pong": NormalPong,
            "Portal Pong": PortalPong,
            "Shatter Pong": ShatterPong,
            "Split Pong": SplitPong,
            "Omnidirectional Pong": OmnidirectionalPong
        }
        if not pong_type_to_class.__contains__(pong_type):
            raise ValueError("No such pong type exists: ")

        else:
            return pong_type_to_class.get(pong_type)

    def get_pong_type():
        """ summary: gets the game modes and pong types from the game modes screen and gets the pong type from that
            params: None
            returns: PongType; the pong type that the game screen should use
        """

        # Each Game Mode has a list of possible pong types that are chosen at random after each reset
        # Reset meaning the start of the game or after someone scores
        game_mode_to_pong_types = {
            "Chaos": ["Gravity Pong", "Portal Pong", "Split Pong"],
            "Civilized": ["Normal Pong", "Shatter Pong", "Gravity Pong"],
            "Unique Twist": ["Gravity Pong", "Middle Paddle Pong", "Portal Pong", "Shatter Pong", "Split Pong"],
            "Random": GameModeSelector.all_pong_types
        }
        pong_type = None

        if game_mode_to_pong_types.__contains__(GameModeSelector.game_mode):
            pong_types = game_mode_to_pong_types.get(
                GameModeSelector.game_mode)
            pong_type = GameModeSelector.get_random_pong_type(pong_types)

        elif GameModeSelector.game_mode == "Pick Pong Type":
            pong_type = GameModeSelector.get_pong_type_class(
                GameModeSelector.pong_type)

        return pong_type

    def get_random_pong_type(pong_types):
        """ summary: finds a random pong type and returns it

            params:
                pong_types: List of String; the names of the pong types

            returns: PongType; the pong type that the game screen should play
        """

        pong_type = get_random_item(pong_types)
        return GameModeSelector.get_pong_type_class(pong_type)

    def is_single_player():
        """returns: boolean; if it is Single Player"""

        return GameModeSelector.number_of_players == "Single Player"

    def get_ai_difficulty():
        """returns: int; the difficulty of the AI (a number between 1 and 10)"""

        return GameModeSelector.ai_difficulty
