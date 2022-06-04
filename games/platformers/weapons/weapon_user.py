import abc

from base.drawable_objects import GameObject
from base.engines import CollisionsFinder
from base.important_variables import screen_length
from base.velocity_calculator import VelocityCalculator


class WeaponUser(GameObject):
    """A class that provides what is needed for a weapon to function"""

    max_velocity = 0
    is_facing_right = False
    hit_points_left = 0
    total_hit_points = 0
    weapon = None
    weapon_index_offset = 1
    index_of_user = 0
    index = 0
    is_on_platform = True
    sub_components = []

    # Collision Data
    left_collision_data = []
    right_collision_data = []
    top_collision_data = []
    bottom_collision_data = []
    components = []

    def __init__(self, x_coordinate=0, y_coordinate=0, height=0, length=0, color=(0, 0, 0)):
        """Initializes the object"""

        super().__init__(x_coordinate, y_coordinate, height, length, color)
        self.sub_components = [self]
        self.components = []

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

    @property
    def user_type(self):
        return self.object_type

    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
        """Runs what should happen when the weapon and an inanimate object collide"""

        self.weapon.run_inanimate_object_collision(inanimate_object, index_of_sub_component - 1, time)

    def run_enemy_collision(self, enemy, index_of_sub_component):
        """Runs what should happen when the weapon user hits an 'enemy' (the user would be the enemy's 'enemy')"""

        if index_of_sub_component == self.index_of_user:
            enemy.cause_damage(self.damage)

        elif self.weapon is not None:
            self.weapon.run_enemy_collision(enemy, index_of_sub_component - self.weapon_index_offset)

    def run_upon_activation(self):
        """Runs what should happen when the person who plays the game tries to use the weapon"""

        self.weapon.run_upon_activation()

    def get_sub_components(self):
        """returns: Component[]; all the components that should be ran and rendered"""

        return self.sub_components

    def reset_collision_data(self):
        """Resets all the collision data from the previous cycle, so it can do collisions for this cycle"""

        self.left_collision_data, self.right_collision_data, self.top_collision_data, self.bottom_collision_data = [False, None], [False, None], [False, None], [False, None]

    def get_collision_data(self, inanimate_object, is_collision, time):
        """returns: Boolean[4]; [is_left_collision, is_right_collision, is_top_collision, is_bottom_collision] --> the
           collision data gotten from the inanimate_object and is by the perspective of the user (has the user collided with the inanimate_object's right_edge)"""

        is_same_coordinates = self.right_edge == inanimate_object.x_coordinate or self.x_coordinate == inanimate_object.right_edge
        if inanimate_object.y_coordinate == 300 and self.max_velocity == VelocityCalculator.give_velocity(screen_length, 700):
            CollisionsFinder.is_top_collision(self, inanimate_object, True, time)

        return [CollisionsFinder.is_left_collision(self, inanimate_object, is_collision, time),
                CollisionsFinder.is_right_collision(self, inanimate_object, is_collision, time),
                CollisionsFinder.is_top_collision(self, inanimate_object, is_collision, time) and not is_same_coordinates,
                CollisionsFinder.is_bottom_collision(self, inanimate_object, is_collision, time)]

    def update_collision_data(self, inanimate_object, current_collision_data, is_collision):
        """Updates the values of the 'current_collision_data' to reflect 'is_collision' and 'inanimate_object'"""

        if not current_collision_data[0] and is_collision:
            current_collision_data[0], current_collision_data[1] = is_collision, inanimate_object

    def update_platform_collision_data(self, inanimate_object, time):
        """Updates all the inanimate_object collision data"""

        # NOTE: From here own down *_collision_data[0] is if a user and a inanimate_object have collided
        # and *_collision_data[1] is the inanimate_object the user collided with
        left_collision, right_collision, top_collision, bottom_collision = self.get_collision_data(inanimate_object, True, time)

        self.update_collision_data(inanimate_object, self.left_collision_data, left_collision)
        self.update_collision_data(inanimate_object, self.right_collision_data, right_collision)
        self.update_collision_data(inanimate_object, self.top_collision_data, top_collision)
        self.update_collision_data(inanimate_object, self.bottom_collision_data, bottom_collision)

    def run_collisions(self, time):
        """Runs what should happen based on what got stored in the collision data (nothing is a possibility like possibly an enemy)"""

        pass

    def cause_damage(self, amount):
        """Damages the weapon user by that amount"""

        self.hit_points_left -= amount

