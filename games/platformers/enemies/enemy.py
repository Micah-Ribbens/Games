import abc

from base.drawable_objects import GameObject
from games.platformers.weapons.weapon_user import WeaponUser


class Enemy(WeaponUser, abc.ABC):
    """Anything that harms/attacks the player"""

    damage = 0
    hit_points = 0
    is_on_platform = True
    is_moving_right = True
    sub_components = []
    platform = None
    player = None
    weapon_index_offset = 1
    index_of_enemy = 0

    def __init__(self, damage, hit_points, platform, player, x_coordinate, y_coordinate, length, height):
        """Initializes the object"""

        self.sub_components = [self]
        self.damage, self.hit_points, self.platform = damage, hit_points, platform
        self.player = player
        super().__init__(x_coordinate, y_coordinate, height, length)

    @abc.abstractmethod
    def hit_player(self, player, index_of_sub_component):
        pass

    @abc.abstractmethod
    def hit_by_player(self, player_weapon, index_of_sub_component):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def get_sub_components(self):
        """returns: Component[]; all the components that should be ran and rendered"""

        return self.sub_components

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs what should happen if the enemy or something the player threw hit an inanimate object"""

        if index_of_sub_component != self.index_of_enemy:
            self.run_inanimate_object_collision(inanimate_object, index_of_sub_component - self.weapon_index_offset)


