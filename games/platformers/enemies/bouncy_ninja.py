from games.platformers.enemies.straight_ninja import StraightNinja
from games.platformers.weapons.bouncy_projectile_thrower import BouncyProjectileThrower


class BouncyNinja(StraightNinja):
    """A ninja that throws projectiles that bounce"""

    def __init__(self, damage, hit_points, platform, players, is_gone):
        """Initializes the object"""

        super().__init__(damage, hit_points, platform, players, is_gone)
        self.weapon = BouncyProjectileThrower(lambda: False, self)

    @property
    def projectile_height(self):
        # Since all players should be the same height, then the first one can be safely chosen
        # because there has to be at least one player
        return self.players[0].height / 2
