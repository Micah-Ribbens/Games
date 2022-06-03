from base.drawable_objects import GameObject, Ellipse
from base.events import TimedEvent
from base.important_variables import screen_height, screen_length
from base.utility_functions import key_is_hit
from base.velocity_calculator import VelocityCalculator
from games.platformers.weapons.weapon import Weapon
from base.engines import CollisionsFinder

class Projectile(Ellipse):
    """A projectile that the projectile thrower uses"""

    size = VelocityCalculator.give_measurement(screen_height, 6)
    length, height = size, size
    is_moving_right = False
    velocity = 0
    is_runnable = False
    is_destroyed = False
    index = 0
    total_hit_points = 0
    hit_points_left = 0
    user = None

    def __init__(self, x_coordinate, y_coordinate, is_moving_right, user_max_velocity, object_type, total_hit_points, user):
        """Initializes the object"""

        super().__init__(x_coordinate, y_coordinate, self.size, self.size)
        self.total_hit_points, self.hit_points_left = total_hit_points, total_hit_points
        self.is_moving_right = is_moving_right
        self.velocity = user_max_velocity + VelocityCalculator.give_measurement(screen_height, 50)
        self.object_type, self.user = object_type, user

    def run(self):
        """Runs all the code for the projectile to move across the screen and other necessary things"""

        distance = VelocityCalculator.calc_distance(self.velocity)
        self.x_coordinate += distance if self.is_moving_right else -distance


class ProjectileThrower(Weapon):
    """A weapon that is used for throwing projectiles"""

    deleted_sub_components_indexes = []
    is_gone = None

    def __init__(self, use_action, user, is_gone):
        """Initializes the object"""

        super().__init__(10, 10, use_action, user, .2, is_gone)
        self.sub_components = []

    def run(self):
        """Runs all the code necessary in order for this object to work"""

        super().run()
        # TODO maybe consider updating this if the game is running slow
        updated_sub_components = []

        for x in range(len(self.sub_components)):
            projectile = self.sub_components[x]

            if not self.is_gone(projectile) and not self.deleted_sub_components_indexes.__contains__(x):
                projectile.run()
                projectile.index = len(updated_sub_components) + self.user.weapon_index_offset
                updated_sub_components.append(projectile)

        self.sub_components = updated_sub_components
        self.deleted_sub_components_indexes = []

    def run_upon_activation(self):
        """Runs the code that should be completed when the code decides to use this weapon"""
        self.sub_components.append(Projectile(self.get_weapon_x_coordinate(Projectile.size, self.user.should_shoot_right),
                                   self.user.projectile_y_coordinate - Projectile.size, self.user.should_shoot_right,
                                   self.user.projectile_velocity, self.object_type, self.total_hit_points, self.user))

    def run_enemy_collision(self, user, index_of_sub_component):
        """Runs the code for figuring out what to do when one of the projectiles hits an enemy"""

        user.cause_damage(self.damage)
        self.deleted_sub_components_indexes.append(index_of_sub_component)

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs all the code for figuring ot what to do when one of the projectiles hits an inanimate object (platforms, trees, etc.)"""

        self.deleted_sub_components_indexes.append(index_of_sub_component)

    def reset(self):
        """Resets everything back to the start of the game"""

        self.sub_components = []




