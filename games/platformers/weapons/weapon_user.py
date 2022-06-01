from base.drawable_objects import GameObject


class WeaponUser(GameObject):
    """A class that provides what is needed for a weapon to function"""

    max_velocity = 0
    is_facing_right = False
    weapon = None

    @property
    def projectile_velocity(self):
        return self.max_velocity

    @property
    def projectile_y_coordinate(self):
        return self.y_midpoint

    @property
    def projectile_height(self):
        return self.height / 2

    @property
    def should_shoot_right(self):
        return self.is_facing_right

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs what should happen when the weapon and an inanimate object collide"""

        self.weapon.run_inanimate_object_collision(inanimate_object, index_of_sub_component - 1)

    def run_upon_activation(self):
        """Runs what should happen when the person who plays the game tries to use the weapon"""

        self.weapon.run_upon_activation()
