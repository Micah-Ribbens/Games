from gui_components.selection_screen import SelectionScreen
from minigames.card_games.long_word_game import CardGame
from minigames.quick_draw import QuickDraw


class StartScreen(SelectionScreen):
    """The screen that is displayed at the start"""

    def __init__(self, height_used_up, length_used_up):
        """Initializes the object"""

        screens = [QuickDraw(height_used_up, length_used_up), CardGame(height_used_up, length_used_up)]
        screen_names = ["Quick Draw", "Card Game"]

        super().__init__(height_used_up, length_used_up, screens, screen_names)