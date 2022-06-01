from base.colors import red, blue, white
from base.dimensions import Dimensions
from base.engines import CollisionsFinder
from base.game_movement import GameMovement
from base.important_variables import *
from base.utility_classes import HistoryKeeper
from base.velocity_calculator import VelocityCalculator
from games.shooting_games.base.bullet import Bullet
from games.shooting_games.base.death_ball import DeathBall
from games.shooting_games.base.player import Player
from gui_components.grid import Grid
from gui_components.screen import Screen
from gui_components.text_box import TextBox
from gui_components.text_box_with_title import TextBoxWithTitle


class ShootingGameScreen(Screen):
    """A simple shooting game that requires dodging a flying ball that kills the player"""

    bullets = []
    player1 = None
    player2 = None
    death_ball = DeathBall()
    base_components = []
    player1_score = 0
    player2_score = 0
    player1_score_field = TextBox("Player 1 Score: ", 20, False, red, white)
    player2_score_field = TextBox("Player 2 Score: ", 20, False, blue, white)

    def __init__(self):
        """Initializes the object"""
        self.player1 = Player(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_g, pygame.K_f)
        self.player2 = Player(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_PERIOD, pygame.K_COMMA)

        self.player1.set_color(red)
        self.player2.set_color(blue)

        self.player2.x_coordinate = screen_length - self.player2.length

        grid = Grid(Dimensions(screen_length * .2, 0, screen_length * .4, screen_height * .1), None, 1, True)
        grid.turn_into_grid([self.player1_score_field, self.player2_score_field], None, None)

        self.base_components = [self.player1_score_field, self.player2_score_field, self.player1, self.player2, self.death_ball]

    def run(self):
        """Runs all the code necessary for this game to run properly"""

        self.player1_score_field.text = f"Player 1 Score: {self.player1_score}"
        self.player2_score_field.text = f"Player 2 Score: {self.player2_score}"
        self.bullets += self.player1.bullets + self.player2.bullets

        self.components = self.base_components + self.bullets

        self.add_needed_objects()
        self.run_players_movement()
        self.run_bullet_collisions()

    def add_needed_objects(self):
        """Adds all the object to the HistoryKeeper"""

        HistoryKeeper.add(self.player1, self.player1.name, True)
        HistoryKeeper.add(self.player2, self.player2.name, True)
        HistoryKeeper.add(self.death_ball, self.death_ball.name, True)

        for bullet in self.bullets:
            bullet.name = id(bullet)
            HistoryKeeper.add(bullet, bullet.name, True)

    def run_players_movement(self):
        """Runs the players movement"""

        # So the player's turrets aren't touching and there is a decent amount of space between them; divide by two
        # Because both players combined equals the full buffer
        buffer = (self.player1.turret.length * 2 + VelocityCalculator.give_measurement(screen_length, 2)) / 2

        middle_of_screen = screen_length / 2

        player1_max_x_coordinate = middle_of_screen - buffer
        player2_min_x_coordinate = middle_of_screen + buffer

        GameMovement.set_player_vertical_movement(self.player1, screen_height, 0)
        GameMovement.set_player_vertical_movement(self.player2, screen_height, 0)

        GameMovement.set_player_horizontal_movement(self.player1, player1_max_x_coordinate, 0)
        GameMovement.set_player_horizontal_movement(self.player2, screen_length, player2_min_x_coordinate)

    def run_bullet_collisions(self):
        """Runs the collisions for the bullets"""

        base_stun_time = .4

        for i in range(len(self.bullets)):
            stun_time = base_stun_time * self.bullets[i].total_hits_to_destroy
            bullet1: Bullet = self.bullets[i]

            bullet_has_hit_player1 = CollisionsFinder.is_collision(self.player1, bullet1)
            bullet_has_hit_player2 = CollisionsFinder.is_collision(self.player2, bullet1)
            bullet_has_hit_death_ball = CollisionsFinder.is_collision(bullet1, self.death_ball)

            if bullet_has_hit_player1:
                # The bigger the bullet the longer the stun time should be
                self.player1.stun(stun_time)

            elif bullet_has_hit_player2:
                self.player2.stun(stun_time)

            # In order for the bullet to make the death ball change directions it must be going the opposite direction
            if bullet_has_hit_death_ball and self.death_ball.is_moving_right != bullet1.is_moving_right:
                self.death_ball.hits_left_to_change_direction -= bullet1.total_hits_to_destroy

            if bullet_has_hit_player1 or bullet_has_hit_player2 or bullet_has_hit_death_ball:
                bullet1.hits_left_to_destroy = 0
                continue

            for j in range(len(self.bullets) - i):
                bullet2: Bullet = self.bullets[j + i]

                # For speed; don't have to check collision if the bullets don't have health left
                if bullet2.hits_left_to_destroy <= 0 or bullet1.hits_left_to_destroy <= 0:
                    continue

                if bullet1 != bullet2 and CollisionsFinder.is_collision(bullet1, bullet2):
                    bullet1.hits_left_to_destroy -= bullet2.total_hits_to_destroy
                    bullet2.hits_left_to_destroy -= bullet2.total_hits_to_destroy

        self.bullets = list(filter(lambda item: item.hits_left_to_destroy > 0, self.bullets))
