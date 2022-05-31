from base.dimensions import Dimensions
from base.drawable_objects import GameObject
import abc


# TODO come back to figuring out what weapons should do
from base.events import Event, TimedEvent
from base.utility_functions import key_is_hit


class Weapon(abc.ABC):
    """Something the player can use to hit enemies or anything else"""

    damage = 10
    hit_points = 10
    use_key = None
    use_key_event = None
    player = None
    sub_components = []
    is_runnable = False
    wait_event = None

    def __init__(self, damage, hit_points, use_key, player, cool_down_time):
        """Initilizes the object"""

        self.use_key_event = Event()
        self.damage, self.hit_points, self.use_key = damage, hit_points, use_key
        self.player = player
        self.name = id(self)
        self.wait_event = TimedEvent(cool_down_time, False)
        self.sub_components = [self]

    def run(self):
        self.use_key_event.run(key_is_hit(self.use_key))
        self.wait_event.run(self.wait_event.current_time >= self.wait_event.time_needed, False)

        if self.use_key_event.is_click() and self.wait_event.has_finished():
            self.run_upon_activation()
            self.wait_event.start()

    def get_sub_components(self):
        """returns: GameObject[0]; all the sub components that must be rendered and have collisions for"""

        return self.sub_components

    def get_weapon_x_coordinate(self, horizontal_length, is_facing_right):
        """returns: x_coordinate; the recommended x coordinate that the weapon should be at (right on the player)"""

        return self.player.right_edge if is_facing_right else self.player.x_coordinate - horizontal_length

    @abc.abstractmethod
    def run_player_collision(self, player, index_of_sub_component):
        """Runs what should happen when the player and the weapon collide"""
        pass

    @abc.abstractmethod
    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component):
        """Runs what should happen when the weapon and an inanimate object collide"""
        pass

    @abc.abstractmethod
    def run_upon_activation(self):
        """Runs what should happen when the person who plays the game tries to use the weapon"""
        pass

