from games.platformers.enemies.straight_ninja import StraightNinja
from games.platformers.weapons.bouncy_projectile_thrower import BouncyProjectileThrower


class BouncyNinja(StraightNinja):
    """A ninja that throws projectiles that bounce"""

    def __init__(self, damage, hit_points, platform, player):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, player)
        self.weapon = BouncyProjectileThrower(lambda: False, self)


    @property
    def projectile_height(self):
        return self.player.height / 2