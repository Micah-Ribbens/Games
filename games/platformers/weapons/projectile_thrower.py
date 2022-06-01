from base.drawable_objects import GameObject, Ellipse
from base.events import TimedEvent
from base.important_variables import screen_height, screen_length
from base.utility_functions import key_is_hit
from base.velocity_calculator import VelocityCalculator
from games.platformers.weapons.weapon import Weapon


class Projectile(Ellipse):
    """A projectile that the projectile thrower uses"""

    size = VelocityCalculator.give_measurement(screen_height, 6)
    length, height = size, size
    is_moving_right = False
    velocity = 0
    is_runnable = False
    is_destroyed = False

    def __init__(self, x_coordinate, y_coordinate, is_moving_right, player_max_velocity):
        """Initializes the object"""

        super().__init__(x_coordinate, y_coordinate, self.size, self.size)
        self.is_moving_right = is_moving_right
        self.velocity = player_max_velocity + VelocityCalculator.give_measurement(screen_height, 50)

    def run(self):
        """Runs all the code for the projectile to move across the screen and other necessary things"""

        distance = VelocityCalculator.calc_distance(self.velocity)
        self.x_coordinate += distance if self.is_moving_right else -distance


class ProjectileThrower(Weapon):
    """A weapon that is used for throwing projectiles"""

    def __init__(self, use_key_action, player):
        """Initializes the object"""

        super().__init__(10, 10, use_key_action, player, .2)
        self.sub_components = []

    def run(self):
        """Runs all the code necessary in order for this object to work"""

        super().run()
        # TODO maybe consider updating this if the game is running slow
        updated_sub_components = []
        for x in range(len(self.sub_components)):
            projectile = self.sub_components[x]
            projectile.run()

            if projectile.right_edge > 0 and projectile.x_coordinate < screen_length:
                updated_sub_components.append(projectile)

        self.sub_components = updated_sub_components

    def run_upon_activation(self):
        """Runs the code that should be completed when the code decides to use this weapon"""

        self.sub_components.append(Projectile(self.get_weapon_x_coordinate(Projectile.size, self.player.should_shoot_right),
                                              self.player.projectile_y_coordinate - Projectile.size, self.player.should_shoot_right, self.player.projectile_velocity))

    def run_player_collision(self, player, index_of_sub_component):
        """Runs the code for figuring out what to do when one of the projectiles hits a player"""

        player.hit_points -= self.damage
        del self.sub_components[index_of_sub_component]

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs all the code for figuring ot what to do when one of the projectiles hits an inanimate object (platforms, trees, etc.)"""

        del self.sub_components[index_of_sub_component]





