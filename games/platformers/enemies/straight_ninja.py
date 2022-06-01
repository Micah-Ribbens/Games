from base.equations import Point
from base.important_variables import screen_length, screen_height
from base.path import VelocityPath, ActionPath
from base.velocity_calculator import VelocityCalculator
from games.platformers.enemies.enemy import Enemy
from games.platformers.weapons.bouncy_projectile_thrower import BouncyProjectileThrower
from games.platformers.weapons.projectile_thrower import Projectile, ProjectileThrower


class StraightNinja(Enemy):
    path = None
    velocity = VelocityCalculator.give_velocity(screen_length, 300)
    length = VelocityCalculator.give_measurement(screen_length, 5)
    height = VelocityCalculator.give_measurement(screen_height, 10)
    weapon = None
    is_facing_right = None
    index_of_enemy = 0
    weapon_index_offset = 1

    def __init__(self, damage, hit_points, platform, player):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, player, 0, 0, self.length, self.height)

        y_coordinate = platform.y_coordinate - self.height
        wait_time = .5
        self.path = ActionPath(Point(platform.right_edge - self.length, y_coordinate), self, self.velocity)
        self.path.add_point(Point(platform.x_coordinate, y_coordinate), lambda: [])
        self.path.add_point(Point(platform.x_coordinate, y_coordinate), self.shoot_star, wait_time)
        self.path.add_point(Point(platform.right_edge - self.length, y_coordinate), lambda: [])
        self.path.add_point(Point(platform.right_edge - self.length, y_coordinate), self.shoot_star, wait_time)

        self.path.is_unending = True
        self.weapon = ProjectileThrower(lambda: False, self)

    def hit_player(self, player, index_of_sub_component):
        pass

    def hit_by_player(self, player_weapon, index_of_sub_component):
        pass

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs what should happen when the enemy or its projectiles hits an inanimate object"""

        if index_of_sub_component != self.index_of_enemy:
            self.weapon.run_inanimate_object_collision(inanimate_object, index_of_sub_component - self.weapon_index_offset)

    def run(self):
        """Runs everything necessary in order for this enemy to work"""

        self.sub_components = [self] + self.weapon.get_sub_components()
        self.path.run()
        self.weapon.run()

    def shoot_star(self):
        """Shoots a star"""

        # Casting to int prevents a rounding error (off by .000000001 or less)
        self.is_facing_right = int(self.x_coordinate) == int(self.platform.x_coordinate)

        # Sometimes there is a bad lag spike, so the enemy won't stop meaning then I have to check if the player
        # Is now moving right (slope of the x coordinate line is increasing means the x coordinates are increasing)
        if int(self.x_coordinate) != int(self.platform.x_coordinate) and int(self.right_edge) != int(self.platform.right_edge):
            self.is_facing_right = self.path.x_coordinate_lines[self.path.get_index_of_line(self.path.total_time)].slope_is_positive()

        self.weapon.run_upon_activation()

    def get_sub_components(self):
        """returns: Component[]; all the components that should be rendered and ran"""

        return [self] + self.weapon.get_sub_components()

    @property
    def projectile_velocity(self):
        return self.velocity


