from base.dimensions import Dimensions
from base.engines import CollisionsFinder
from base.utility_classes import HistoryKeeper
from games.platformers.base.gravity_engine import GravityEngine
from games.platformers.base.platform import Platform
from games.platformers.base.player import Player
from games.platformers.enemies.charging_bull import ChargingBull
from games.platformers.enemies.straight_ninja import StraightNinja
from games.platformers.enemies.bouncy_ninja import BouncyNinja
from gui_components.grid import Grid
from gui_components.health_bar import HealthBar
from gui_components.screen import Screen
from games.platformers.base.platformer_variables import *


class PlatformerScreen(Screen):
    """A basic platformer game"""

    players = []
    player_health_bars = []
    enemies = []
    platforms = []
    game_objects = []
    gravity_engine = None

    def __init__(self):
        """Initializes the object"""

        health_grid = Grid(Dimensions(0, 0, screen_length * .25, screen_height * .1), 2, 2, True)
        self.players = [Player(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_f, self.is_gone)]
        self.setup_enemies_and_platforms()
        self.gravity_engine = GravityEngine(self.players, self.players[0].jumping_path.acceleration)

        for player in self.players:
            player.gravity_engine = self.gravity_engine
            player.x_coordinate = self.platforms[0].x_coordinate + 10
            player.base_y_coordinate = self.platforms[0].y_coordinate - player.height
            player.set_y_coordinate(player.base_y_coordinate)

            self.player_health_bars.append(HealthBar(player, lambda: False))

        health_grid.turn_into_grid(self.player_health_bars, None, None)

    def setup_enemies_and_platforms(self):
        """Creates the enemies and platforms of the game for starting out"""

        # Platform above you
        # self.platforms = [Platform(), Platform(Platform().x_coordinate, Platform().y_coordinate - self.players[0].max_jump_height * 1/2 - 200 - self.players[0].height, screen_length, 200, True)]

        # Two normal platforms
        # self.platforms = [Platform(), Platform(Platform().right_edge + 200, Platform().y_coordinate - self.players[0].max_jump_height, 200, 200, True)]

        # One Long Platform
        # self.platforms = [Platform(100, 300, 800, 100, True)]

        # Sandwich Platform
        self.platforms = [Platform(100, 300, 800, 100, True), Platform(0, 200, 100, 100, True), Platform(910, 200, 100, 100, True)]

        self.enemies = [BouncyNinja(10, 20, self.platforms[0], self.players, self.is_gone)]

    def run(self):
        """Runs all the code necessary in order for the platformer to work"""

        self.gravity_engine.run()
        self.update_game_objects()

        if HistoryKeeper.is_populated(self.game_objects):
            self.run_all_collisions()

            # All the enemies and players should do something based on the updated collision they got from 'self.run_all_collisions()'
            for game_object in self.enemies + self.players:
                game_object.run_collisions()

        self.add_game_objects()

    def update_game_objects(self):
        """Runs the necessary code to prepare for collisions and some other miscellaneous stuff like making sure
        killed enemies are put onto the screen and resetting the game if the player dies"""

        player_components = []
        for player in self.players:
            if player.hit_points_left <= 0 or not self.within_screen(player):
                self.reset_game()

            player_components += player.get_sub_components()
            player.run()
            player.reset_collision_data()

        updated_enemies = []
        enemy_components = []
        for enemy in self.enemies:
            enemy.reset_collision_data()
            if enemy.hit_points_left > 0 and self.within_screen(enemy):
                updated_enemies.append(enemy)
                enemy_components += enemy.get_sub_components()

        self.enemies = updated_enemies
        self.game_objects = player_components + enemy_components + self.platforms

    def reset_game(self):
        """Resets the game after the player's death"""

        for player in self.players:
            player.reset()

        self.setup_enemies_and_platforms()
        self.gravity_engine.reset()
        HistoryKeeper.last_objects = {}

    def run_all_collisions(self):
        """Runs all the collisions between the player, projectiles, and enemies"""

        # TODO maybe could make this quicker, but not sure if it is worth it
        for i in range(len(self.game_objects)):
            object1 = self.game_objects[i]
            # Only the objects that can be added to the History Keeper should be checked for a collision; also
            # The platforms don't need to check to see if they collided with other objects because if something
            # Collides with the platform it won't do anything in reaction
            if not object1.is_addable or self.is_platform(object1):
                continue

            for j in range(len(self.game_objects)):
                object2 = self.game_objects[j]

                collision_is_possible = object2.is_addable and len(object1.object_type) != len(object2.object_type)
                if collision_is_possible and CollisionsFinder.is_collision(object1, object2):
                    self.run_object_collisions(object1, object2)

    def run_object_collisions(self, main_object, other_object):
        """Runs the collisions between the 'main_object' and the 'other_object;' the main_object acts upon the other_object.
        By act upon I mean damages the other_object, moves the other_object, etc."""

        self.run_user_weapon_inanimate_collisions(self.is_player_weapon(main_object), self.is_player(main_object), main_object, other_object)
        self.run_user_weapon_inanimate_collisions(self.is_enemy_weapon(main_object), self.is_enemy(main_object), main_object, other_object)

        if self.is_enemy(main_object) and self.is_player(other_object):
            main_object.run_enemy_collision(other_object, main_object.index)

        if self.is_enemy_weapon(main_object) and self.is_player(other_object):
            main_object.user.run_enemy_collision(other_object, main_object.index)

        if self.is_enemy_weapon(main_object) and self.is_platform(other_object):
            main_object.user.run_inanimate_object_collision(other_object, main_object.index)

        if self.is_player_weapon(main_object) and self.is_enemy(other_object):
            main_object.user.run_enemy_collision(other_object, main_object.index)

        # Doing it this way, so a collision does not happen twice - once when the player_weapon is the main_object
        # And the other where the enemy_weapon is the main_object.
        if self.is_player_weapon(main_object) and self.is_enemy_weapon(other_object):
            main_object.user.run_enemy_collision(other_object, main_object.index)

        if self.is_enemy_weapon(main_object) and self.is_enemy_weapon(other_object):
            main_object.user.run_enemy_collision(other_object, main_object.index)

    def run_user_weapon_inanimate_collisions(self, is_weapon, is_user, user_or_weapon, other_object):
        """Runs the collisions between the user + the user's weapon and inanimate objects"""

        if is_user and self.is_platform(other_object):
            user_or_weapon.run_inanimate_object_collision(other_object, user_or_weapon.index)

        if is_weapon and self.is_platform(other_object):
            user_or_weapon.user.run_inanimate_object_collision(other_object, user_or_weapon.index)

    def add_game_objects(self):
        """Adds all the game objects to the HistoryKeeper"""

        for player in self.players:
            self.add_sub_components(player.get_sub_components())

        self.add_sub_components(self.platforms)

        for enemy in self.enemies:
            self.add_sub_components(enemy.get_sub_components())

    def add_sub_components(self, component_list):
        """Adds all the components in the component_list to the History Keeper"""

        for component in component_list:
            if component.is_addable:
                component.name = id(component)
                HistoryKeeper.add(component, component.name, True)

    def get_components(self):
        """returns: Component[]; all the components that should be rendered"""

        if len(self.enemies) != 0:
            return self.player_health_bars + self.platforms + self.players[0].get_sub_components() + self.enemies[0].get_components()

        else:
            return self.player_health_bars + self.platforms + self.players[0].get_sub_components()


    def within_screen(self, game_object):
        """returns: boolean; if the game_object is within the screen (can be seen on the screen)"""

        return (game_object.right_edge > 0 and game_object.x_coordinate < screen_length and
                game_object.bottom > 0 and game_object.y_coordinate < screen_height)

    def is_gone(self, game_object):
        """returns: boolean; if the game_object should stop being ran and rendered onto the screen"""

        return game_object.hit_points_left <= 0 or not self.within_screen(game_object)

    # HELPER METHODS FOR COLLISIONS; Since they all have a unique length I can just use the lengths here
    def is_enemy(self, game_object):
        """returns: boolean; if the game_object is just an enemy (not a weapon) --> object type would be 'Enemy'"""

        return len(game_object.object_type) == 5

    def is_enemy_weapon(self, game_object):
        """returns: boolean; if the game_object is an enemy's weapon --> object type would be 'Enemy Weapon'"""

        return len(game_object.object_type) == 12

    def is_player(self, game_object):
        """returns: boolean; if the game_object is the player --> object type would be 'Player'"""

        return len(game_object.object_type) == 6

    def is_player_weapon(self, game_object):
        """returns: boolean; if the game_object is the player's weapon --> object type would be 'Player Weapon'"""

        return len(game_object.object_type) == 13

    def is_platform(self, game_object):
        """returns: boolean; if the game_object is a platform --> object type would be 'Platform'"""

        return len(game_object.object_type) == 8








