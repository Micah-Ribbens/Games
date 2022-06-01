from abc import ABC

from base.drawable_objects import Ellipse
from base.engines import CollisionsFinder
from base.important_variables import screen_height
from base.quadratic_equations import PhysicsPath
from base.utility_classes import HistoryKeeper
from games.platformers.weapons.projectile_thrower import Projectile, ProjectileThrower
from games.platformers.weapons.weapon import Weapon
from games.platformers.base.platformer_variables import *


class BouncyProjectile(Projectile):
    """A projectile that bounces"""

    projectile_path = None

    def __init__(self, x_coordinate, y_coordinate, is_moving_right, projectile_height, player_velocity):
        """Initializes the object"""

        super().__init__(x_coordinate, y_coordinate, is_moving_right, player_velocity)
        time_to_vertex = .2
        self.projectile_path = PhysicsPath(self, "y_coordinate", -projectile_height, y_coordinate - self.height, time_to_vertex)
        self.projectile_path.set_initial_distance(y_coordinate - self.height)
        self.projectile_path.current_time = time_to_vertex

    def run(self):
        """Runs all the code necessary in order for this object to work properly"""

        super().run()
        self.projectile_path.run(False, True, True)

    def run_collision(self, y_coordinate):
        """Runs all the code for figuring out what should happen when the ball collides with something by going down"""

        self.projectile_path.set_initial_distance(y_coordinate - self.height)
        self.projectile_path.reset()

        # So it lets the game know where the ball was previously; makes sure a collision doesn't happen next cycle
        # Because the ball was inside the platform when it wasn't
        self.y_coordinate = y_coordinate - self.height


class BouncyProjectileThrower(ProjectileThrower):
    """A projectile thrower except the projectiles bounce"""

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs all the code for figuring ot what to do when one of the projectiles hits an inanimate object (platforms, trees, etc.)"""

        projectile: BouncyProjectile = self.sub_components[index_of_sub_component]

        if CollisionsFinder.is_top_collision(projectile, inanimate_object, True):
            projectile.run_collision(inanimate_object.y_coordinate)

        else:
            del self.sub_components[index_of_sub_component]

    def run_upon_activation(self):
        """Runs the code that should be completed when the code decides to use this weapon"""

        self.sub_components.append(BouncyProjectile(self.get_weapon_x_coordinate(Projectile.size, self.player.should_shoot_right),
                                                    self.player.projectile_y_coordinate, self.player.should_shoot_right, self.player.projectile_height, self.player.projectile_velocity))

