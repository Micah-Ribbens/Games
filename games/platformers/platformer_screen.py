from base.engines import CollisionsFinder
from base.utility_classes import HistoryKeeper
from games.platformers.base.gravity_engine import GravityEngine
from games.platformers.base.platform import Platform
from games.platformers.base.player import Player
from games.platformers.enemies.charging_bull import ChargingBull
from games.platformers.enemies.straight_ninja import StraightNinja
from gui_components.screen import Screen
from games.platformers.base.platformer_variables import *


class PlatformerScreen(Screen):
    """A basic platformer game"""

    player = Player(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_f)
    gravity_engine = None
    enemy = None
    platforms = []

    def __init__(self):
        """Initializes the object"""

        # Platform above you
        # self.platforms = [Platform(), Platform(Platform().x_coordinate, Platform().y_coordinate - self.player.max_jump_height * 1/2 - 200 - self.player.height, screen_length, 200, True)]

        # Two normal platforms
        # self.platforms = [Platform(), Platform(Platform().right_edge + 200, Platform().y_coordinate - self.player.max_jump_height, 200, 200, True)]

        # One Long Platform
        # self.platforms = [Platform(100, 300, 800, 100, True)]

        # Sandwich Platform
        self.platforms = [Platform(100, 300, 800, 100, True), Platform(0, 200, 100, 100, True), Platform(910, 200, 100, 100, True)]

        self.player.x_coordinate = self.platforms[0].x_coordinate
        self.gravity_engine = GravityEngine([self.player], self.player.jumping_path.acceleration)

        self.player.base_y_coordinate = self.platforms[0].y_coordinate - self.player.height
        self.player.set_y_coordinate(self.player.base_y_coordinate)

        self.enemy = ChargingBull(20, 20, self.platforms[0], self.player)
        self.components = [self.player] + self.platforms + self.player.weapon.get_sub_components() + self.enemy.get_sub_components()

    def run(self):
        """Runs all the code necessary in order for the platformer to work"""

        self.player.run()

        if self.player.y_coordinate >= screen_height:
            self.reset_game()

        self.gravity_engine.run()
        self.run_all_collisions()

        self.add_game_objects()
        self.components = [self.player] + self.platforms + self.player.weapon.get_sub_components() + self.enemy.get_sub_components()

    # TODO figure out what should be reset
    def reset_game(self):
        """Resets the game after the player's death"""

        self.player.reset()
        self.gravity_engine.reset()
        HistoryKeeper.last_objects = {}

    def run_all_collisions(self):
        """Runs all the collisions between the player, projectiles, and enemies"""

        self.run_platform_collisions()
        player_weapon = self.player.weapon

        for platform in self.platforms:
            self.run_platform_owner_collisions(player_weapon.get_sub_components(), platform, player_weapon)
            self.run_platform_owner_collisions(self.enemy.get_sub_components(), platform, self.enemy)

    def run_platform_owner_collisions(self, sub_components, platform, owner):
        """Runs all the collisions between an owner of the sub_components and a platform"""

        for x in range(len(sub_components)):
            sub_component = sub_components[x]
            if CollisionsFinder.is_collision(platform, sub_component):
                owner.run_inanimate_object_collision(platform, x)

    def run_platform_collisions(self):
        """Runs all the collisions between the player and the platforms"""

        left_collision_data, right_collision_data, top_collision_data, bottom_collision_data = self.get_platform_collision_data()
        self.alter_player_horizontal_movement(left_collision_data, right_collision_data)
        self.alter_player_vertical_movement(top_collision_data, bottom_collision_data)

    def change_player_attribute_if(self, condition, attribute_changing_function, value):
        """Changes the player's attribute if the condition is True otherwise it does nothing"""

        if condition:
            attribute_changing_function(value)

    def get_collision_data(self, platform, is_collision):
        """returns: Boolean[4]; [is_left_collision, is_right_collision, is_top_collision, is_bottom_collision] --> the
           collision data gotten from the platform and is by the perspective of the player (has the player collided with the platform's right_edge)"""

        return [CollisionsFinder.is_left_collision(self.player, platform, is_collision),
                CollisionsFinder.is_right_collision(self.player, platform, is_collision),
                CollisionsFinder.is_top_collision(self.player, platform, is_collision),
                CollisionsFinder.is_bottom_collision(self.player, platform, is_collision)]

    def get_updated_collision_data(self, platform, current_collision_data, is_collision):
        """returns: Object[2]; the collision data --> [is_collision, platform_collided_with (if applicable)]"""

        if is_collision and current_collision_data[0]:
            print("VEEEEEEERY BAD THIS SHOULD NOT HAPPEN LIKE EVER HOW CAN IT COLLIDE WITH TWO PLATFORMS?......................")

        return_value = current_collision_data

        if not current_collision_data[0]:
            return_value = [is_collision, platform]

        return return_value

    def get_platform_collision_data(self):
        """returns: Object[4][Boolean, platform]; [left_collision_data, right_collision_data, top_collision_data, bottom_collision_data]"""

        # Just initializing these variables
        left_collision_data, right_collision_data, top_collision_data, bottom_collision_data = [False, None], [False, None], [False, None], [False, None]

        # NOTE: From here own down *_collision_data[0] is if a player and a platform have collided
        # and *_collision_data[1] is the platform the player collided with
        for platform in self.platforms:
            is_collision = CollisionsFinder.is_collision(self.player, platform)
            left_collision, right_collision, top_collision, bottom_collision = self.get_collision_data(platform, is_collision)

            left_collision_data = self.get_updated_collision_data(platform, left_collision_data, left_collision)
            right_collision_data = self.get_updated_collision_data(platform, right_collision_data, right_collision)
            top_collision_data = self.get_updated_collision_data(platform, top_collision_data, top_collision)
            bottom_collision_data = self.get_updated_collision_data(platform, bottom_collision_data, bottom_collision)

        return [left_collision_data, right_collision_data, top_collision_data, bottom_collision_data]

    def alter_player_horizontal_movement(self, left_collision_data, right_collision_data):
        """Alters the player's horizontal movement so it stays within the screen and is not touching the platforms"""

        player_is_beyond_screen_left = self.player.x_coordinate <= 0
        player_is_beyond_screen_right = self.player.right_edge >= screen_length

        self.player.can_move_left = not right_collision_data[0] and not player_is_beyond_screen_left
        self.player.can_move_right = not left_collision_data[0] and not player_is_beyond_screen_right

        # Setting the player's x coordinate if the any of the above conditions were met (collided with platform or beyond screen)
        function = self.player.set_x_coordinate
        self.change_player_attribute_if(player_is_beyond_screen_left, function, 0)
        self.change_player_attribute_if(player_is_beyond_screen_right, function, screen_length - self.player.length)
        self.change_player_attribute_if(right_collision_data[0], function, right_collision_data[1].right_edge)
        self.change_player_attribute_if(left_collision_data[0], function, left_collision_data[1].x_coordinate - self.player.length)

    def alter_player_vertical_movement(self, top_collision_data, bottom_collision_data):
        """Alters the player's vertical movement so it can't go through platforms"""

        player_is_on_platform = top_collision_data[0]

        if player_is_on_platform:
            self.player.set_y_coordinate(top_collision_data[1].y_coordinate - self.player.height)

        # If collisions can't be detected yet because things have not been added to the HistoryKeeper
        # then the game should just assume the player is on the platform (would only happen the first frame)
        if not HistoryKeeper.is_populated(self.platforms + [self.player]):
            player_is_on_platform = True

        self.player.set_is_on_platform(player_is_on_platform)

        # Moving the player ever so slightly, so that the right and left collisions don't trigger when the player is on
        # The very edge of the platform
        if player_is_on_platform and top_collision_data[1].right_edge == self.player.x_coordinate:
            self.player.x_coordinate -= pow(10, -9)

        if player_is_on_platform and top_collision_data[1].x_coordinate == self.player.right_edge:
            self.player.x_coordinate += pow(10, -9)

        if bottom_collision_data[0]:
            self.gravity_engine.game_object_to_physics_path[self.player].reset()
            self.player.run_bottom_collision(bottom_collision_data[1].bottom)

    def add_game_objects(self):
        """Adds all the game objects to the HistoryKeeper"""

        HistoryKeeper.add(self.player, self.player.name, True)
        self.add_sub_components(self.platforms)
        self.add_sub_components(self.player.weapon.get_sub_components())
        self.add_sub_components(self.enemy.sub_components)

    def add_sub_components(self, component_list):
        """Adds all the components in the component_list to the History Keeper"""

        for component in component_list:
            component.name = id(component)
            HistoryKeeper.add(component, component.name, True)







