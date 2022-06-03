import abc

from base.drawable_objects import GameObject
from games.platformers.weapons.weapon_user import WeaponUser
from gui_components.health_bar import HealthBar


class Enemy(WeaponUser, abc.ABC):
    """Anything that harms/attacks the player"""

    damage = 0
    is_moving_right = True
    platform = None
    players = None
    damage = 10
    health_bar = None
    object_type = "Enemy"
    is_gone = None

    def __init__(self, damage, hit_points, platform, players, x_coordinate, y_coordinate, length, height, is_gone):
        """Initializes the object"""

        self.damage, self.platform = damage, platform
        self.total_hit_points, self.hit_points_left = hit_points, hit_points
        self.players = players
        super().__init__(x_coordinate, y_coordinate, height, length)
        self.health_bar = HealthBar(self)
        self.sub_components = [self]
        self.components = [self, self.health_bar]
        self.is_gone = is_gone

    @abc.abstractmethod
    def run(self):
        pass

    def get_sub_components(self):
        """returns: Component[]; all the components that are collidable"""

        return self.sub_components

    def get_components(self):
        """returns: Component[]; all the components that should be ran and rendered"""

        return self.components

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs what should happen if the enemy or something the player threw hit an inanimate object"""

        if index_of_sub_component != self.index_of_user:
            self.run_inanimate_object_collision(inanimate_object, index_of_sub_component - self.weapon_index_offset)


