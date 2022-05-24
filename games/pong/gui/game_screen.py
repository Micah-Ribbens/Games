from base.utility_classes import HistoryKeeper
from games.pong.base_pong.score_keeper import ScoreKeeper
from games.pong.base_pong.players import Player, AI
from games.pong.base_pong.ball import Ball
from base.important_variables import *
from base.colors import *
from games.pong.pong_types.game_mode_selector import GameModeSelector
from games.pong.pong_types.pong_type import PongType
from gui_components.screen import Screen
from base.pause_button import PauseButton


# Game Screen as in where the game is actually played not selection screens and the sort
class GameScreen(Screen):
    """The screen where the game is played on"""

    pong_type: PongType = None
    pause_is_held_down = False
    game_paused = False
    ball = Ball()
    player1 = Player()
    player2 = Player()
    player1_score = 0
    player2_score = 0
    pause_button = PauseButton()
    components = [player1, player2, ball, pause_button]

    def setup(self):
        """ summary: set ups all the properties of this screen and the game objects
            params: None
            returns: None
        """

        pong_type_class = GameModeSelector.get_pong_type()

        if GameModeSelector.is_single_player():
            self.player2 = AI(GameModeSelector.ai_difficulty, self.ball)
            self.player2.reset()
            self.player2.set_pong_type(self.pong_type)
            self.components = [self.player1, self.player2, self.ball, self.pause_button]

        self.pong_type = pong_type_class(self.player1, self.player2, self.ball)
        self.ball.reset()
        self.player1_score = 0
        self.player2_score = 0
        self.pong_type.reset()
        self.ball.name = "ball"
        self.player2.color = blue
        self.player1.color = red
        self.player1.name = "player1"
        self.player2.name = "player2"
        self.player1.up_key = pygame.K_w
        self.player1.down_key = pygame.K_s
        self.player1.right_key = pygame.K_d
        self.player1.left_key = pygame.K_a
        self.player2.x_coordinate = screen_length - self.player2.length
        HistoryKeeper.reset()
        self.ball.reset()
        self.pong_type.reset()

        self.player2.y_coordinate = screen_height - self.player2.height

    def run(self):
        """ summary: runs all the code for the game objects and just general game stuff
            params: None
            returns: None
        """

        ScoreKeeper.show_score(self.player1_score,
                               self.player2_score)

        self.pong_type.run()

        if self.pong_type.player1_has_scored():
            self.player1_score += 1
            self.reset_after_scoring()
            self.ball.is_moving_right = False

        if self.pong_type.player2_has_scored():
            self.player2_score += 1
            self.reset_after_scoring()
            self.ball.is_moving_right = True

        self.pong_type.add_needed_objects()

    def reset_after_scoring(self):
        """ summary: resets everything after someone has scored
            params: None
            returns: None
        """

        HistoryKeeper.reset()
        self.ball.reset()
        self.pong_type.reset()
        self.player2.reset()
