from base.important_variables import screen_height, screen_length
from base.utility_functions import key_is_hit
from base.velocity_calculator import VelocityCalculator


class GameMovement:
    """A class that gives helper methods for movement in a game"""

    @staticmethod
    def set_player_vertical_movement(player, max_y_coordinate, min_y_coordinate):
        """Sets the player's movement and y coordinates so it stays within these bounds"""

        player.can_move_down = False if player.bottom >= max_y_coordinate else True
        player.can_move_up = False if player.y_coordinate <= min_y_coordinate else True

        if player.y_coordinate <= min_y_coordinate:
            player.y_coordinate = min_y_coordinate

        if player.bottom >= max_y_coordinate:
            player.y_coordinate = max_y_coordinate - player.height

    @staticmethod
    def set_player_horizontal_movement(player, max_x_coordinate, min_x_coordinate):
        """Sets the player's movement and x coordinates so it stays within these bounds"""

        player.can_move_right = False if player.right_edge >= max_x_coordinate else True
        player.can_move_left = False if player.x_coordinate <= min_x_coordinate else True

        if player.right_edge >= max_x_coordinate:
            player.x_coordinate = max_x_coordinate - player.length

        if player.x_coordinate <= min_x_coordinate:
            player.x_coordinate = min_x_coordinate

    @staticmethod
    def player_horizontal_movement(player, player_velocity, left_key, right_key):
        """Runs the player's horizontal movement"""

        if player.can_move_left and key_is_hit(left_key):
            player.x_coordinate -= VelocityCalculator.calc_distance(player_velocity)

        if player.can_move_right and key_is_hit(right_key) and not key_is_hit(left_key):
            player.x_coordinate += VelocityCalculator.calc_distance(player_velocity)

    @staticmethod
    def player_vertical_movement(player, player_velocity, up_key, down_key, can_move_up=None, can_move_down=None):
        """Runs the player's vertical movement"""

        can_move_up = player.can_move_up if can_move_up is None else can_move_up
        can_move_down = player.can_move_down if can_move_down is None else can_move_down

        if key_is_hit(up_key) and can_move_up:
            player.y_coordinate -= VelocityCalculator.calc_distance(player_velocity)

        if key_is_hit(down_key) and can_move_down:
            player.y_coordinate += VelocityCalculator.calc_distance(player_velocity)

    @staticmethod
    def run_projectile_movement(projectile, forwards_velocity, upwards_velocity):
        """Runs the movement for a projectile that moves horizontally and vertically"""

        horizontal_distance = VelocityCalculator.calc_distance(forwards_velocity)
        vertical_distance = VelocityCalculator.calc_distance(upwards_velocity)

        projectile.x_coordinate += horizontal_distance if projectile.is_moving_right else -horizontal_distance
        projectile.y_coordinate += vertical_distance if projectile.is_moving_down else -vertical_distance

        if projectile.bottom >= screen_height:
            distance_change = projectile.bottom - screen_height
            projectile.is_moving_down = False
            projectile.y_coordinate = screen_height - distance_change - projectile.height

        if projectile.y_coordinate <= 0:
            distance_change = -projectile.y_coordinate
            projectile.y_coordinate = projectile.y_coordinate + distance_change
            projectile.is_moving_down = True


