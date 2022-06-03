from base.engines import CollisionsFinder
from base.game_movement import GameMovement
from base.important_variables import screen_length, screen_height
from base.quadratic_equations import PhysicsPath
from base.velocity_calculator import VelocityCalculator
from games.platformers.enemies.enemy import Enemy


class ChargingBull(Enemy):
    """An enemy that charges at players if it sees it"""

    # Modifiable Numbers
    length = VelocityCalculator.give_measurement(screen_length, 20)
    height = VelocityCalculator.give_measurement(screen_height, 10)
    time_to_get_to_max_velocity = 1
    max_velocity = VelocityCalculator.give_velocity(screen_length, 900)

    acceleration_path = None
    current_velocity = 0

    def __init__(self, damage, hit_points, platform, players, is_gone):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, players, platform.right_edge - self.length,
                         platform.y_coordinate - self.height, self.length, self.height, is_gone)

        self.acceleration_path = PhysicsPath()
        self.acceleration_path.set_acceleration(self.time_to_get_to_max_velocity, self.max_velocity)
        self.is_moving_right = False

    def run(self):
        """Runs all the code for the charging bull"""

        for player in self.players:
            distance = self.x_coordinate - player.right_edge
            distance_needed = VelocityCalculator.give_measurement(screen_length, 45)
            should_charge = distance <= distance_needed and CollisionsFinder.is_height_collision(player, self)

            GameMovement.run_acceleration(self, should_charge, self.acceleration_path)

        charging_bull_distance = VelocityCalculator.calc_distance(self.current_velocity)
        self.x_coordinate += charging_bull_distance if self.is_moving_right else -charging_bull_distance

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs the collision for an inanimate object"""

        is_left_collision = CollisionsFinder.is_left_collision(self, inanimate_object, True)
        is_right_collision = CollisionsFinder.is_right_collision(self, inanimate_object, True)

        if is_left_collision or is_right_collision:
            self.acceleration_path.current_time = self.time_to_get_to_max_velocity / 2

        if is_left_collision:
            self.is_moving_right = False
            self.x_coordinate = inanimate_object.x_coordinate - self.length

        elif is_right_collision:
            self.is_moving_right = True
            self.x_coordinate = inanimate_object.right_edge

    def hit_player(self, player, index_of_sub_component):
        pass

    def hit_by_player(self, player_weapon, index_of_sub_component):
        pass


