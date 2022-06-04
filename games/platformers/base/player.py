from math import sqrt

from base.colors import red, light_gray, white
from base.drawable_objects import Segment
from base.engines import CollisionsFinder
from base.events import Event, TimedEvent
from base.game_movement import GameMovement

from base.quadratic_equations import PhysicsPath
from base.utility_classes import HistoryKeeper
from base.utility_functions import key_is_hit
from base.velocity_calculator import VelocityCalculator
from games.platformers.weapons.bouncy_projectile_thrower import BouncyProjectileThrower
from games.platformers.weapons.projectile_thrower import ProjectileThrower
from games.platformers.weapons.sword import Sword
from games.platformers.base.platformer_variables import *
from games.platformers.weapons.weapon_user import WeaponUser


class Player(WeaponUser):
    # Modifiable numbers
    max_jump_height = displacement
    running_deceleration_time = .3
    base_y_coordinate = 0
    base_x_coordinate = 100
    max_velocity = VelocityCalculator.give_velocity(screen_length, 700)
    time_to_get_to_max_velocity = .3
    total_hit_points = 20
    hit_points_left = total_hit_points
    object_type = "Player"

    # Miscellaneous
    jumping_path = None
    deceleration_path = None
    acceleration_path = None
    jumping_event = None
    right_event = None
    left_event = None
    is_runnable = False
    current_velocity = 0
    normal_upwards_velocity = 0
    paths_and_events = None
    gravity_engine = None
    invincibility_event = None

    # Booleans
    can_move_down = False
    can_move_left = False
    can_move_right = False
    is_on_platform = True
    is_facing_right = True

    # Keys
    left_key = None
    right_key = None
    jump_key = None
    down_key = None
    attack_key = None

    def __init__(self, left_key, right_key, jump_key, down_key, attack_key, is_gone):
        """Initializes the object"""

        self.left_key, self.right_key, self.jump_key = left_key, right_key, jump_key
        self.down_key, self.attack_key = down_key, attack_key

        length = VelocityCalculator.give_measurement(screen_length, 5)
        height = VelocityCalculator.give_measurement(screen_height, 15)
        super().__init__(100, screen_height - 200, height, length, white)

        self.jumping_path = PhysicsPath(game_object=self, attribute_modifying="y_coordinate", height_of_path=-displacement, initial_distance=self.y_coordinate)
        self.jumping_path.set_initial_distance(self.y_coordinate)
        self.acceleration_path = PhysicsPath()
        self.acceleration_path.set_acceleration(self.time_to_get_to_max_velocity, self.max_velocity)
        self.deceleration_path = PhysicsPath(game_object=self, attribute_modifying="x_coordinate", max_time=self.running_deceleration_time)
        self.normal_upwards_velocity = self.jumping_path.initial_velocity

        self.jumping_event, self.right_event, self.left_event = Event(), Event(), Event()

        self.weapon = ProjectileThrower(lambda: key_is_hit(self.attack_key), self, is_gone)
        self.invincibility_event = TimedEvent(1, False)
        self.paths_and_events = [self.jumping_path, self.deceleration_path, self.acceleration_path]

    def run(self):
        """Runs all the code that is necessary for the player to work properly"""

        self.weapon.run()
        self.jumping_event.run(key_is_hit(self.jump_key))
        self.right_event.run(key_is_hit(self.right_key))
        self.left_event.run(key_is_hit(self.left_key))
        self.jumping_path.run(False, False)
        self.sub_components = [self] + self.weapon.get_sub_components()
        self.invincibility_event.run(self.invincibility_event.current_time > self.invincibility_event.time_needed, False)
        # if self.is_on_platform:
        #     self.gravity_engine.game_object_to_physics_path[self].reset()

        if self.jumping_path.has_finished() and self.jumping_event.is_click():
            self.jumping_path.start()
            self.gravity_engine.game_object_to_physics_path[self].reset()

        if self.y_coordinate <= 0:
            self.run_bottom_collision(0)

        if self.right_event.has_stopped() or self.left_event.has_stopped():
            self.decelerate_player(self.right_event.has_stopped())
            self.acceleration_path.reset()

        if self.deceleration_path.has_finished() or self.player_movement_direction_is_same_as_deceleration():
            self.set_current_velocity()
            GameMovement.player_horizontal_movement(self, self.current_velocity, self.left_key, self.right_key)
            self.deceleration_path.reset()

            # Should change the 'is_facing_right' based on player input only if the player is not decelerating, so they can't move
            self.is_facing_right = False if self.left_event.is_click() and self.can_move_left else self.is_facing_right
            self.is_facing_right = True if self.right_event.is_click() and self.can_move_right else self.is_facing_right

        elif self.can_decelerate():
            self.deceleration_path.run(False, False, True)

        # If the player is facing a direction, but the player can't move that direction that means the player can't decelerate or accelerate
        should_reset_paths = (self.is_facing_right and not self.can_move_right) or (not self.is_facing_right and not self.can_move_left)
        if should_reset_paths:
            self.deceleration_path.reset()
            self.acceleration_path.reset()

    def set_is_on_platform(self, is_on_platform):
        """Sets the player's is on platform attribute"""

        if self.is_on_platform != is_on_platform and is_on_platform:
            self.jumping_path.reset()
            self.jumping_path.set_initial_distance(self.y_coordinate)
            self.jumping_path.initial_velocity = self.normal_upwards_velocity

        self.is_on_platform = is_on_platform

    def reset(self):
        """Resets the player back to the start of the game"""

        self.x_coordinate = self.base_x_coordinate
        self.y_coordinate = self.base_y_coordinate
        self.is_on_platform = True
        self.jumping_path.initial_velocity = self.normal_upwards_velocity
        self.hit_points_left = self.total_hit_points
        self.invincibility_event.reset()

        # Resetting the direction the player can move
        self.can_move_left, self.can_move_right, self.can_move_down = False, False, False

        for path_or_event in self.paths_and_events:
            path_or_event.reset()

        self.weapon.reset()

    def set_y_coordinate(self, y_coordinate):
        """Sets the y coordinate of the player"""

        self.jumping_path.set_initial_distance(y_coordinate)
        self.y_coordinate = y_coordinate

    def decelerate_player(self, is_moving_right):
        """Makes the player decelerate"""

        self.deceleration_path.initial_distance = self.x_coordinate
        self.deceleration_path.initial_velocity = self.current_velocity if is_moving_right else -self.current_velocity
        self.is_facing_right = is_moving_right

        # If the player is not at maximum velocity it shouldn't take as long to decelerate
        fraction_of_max_velocity = self.max_velocity / self.current_velocity
        time_needed = self.running_deceleration_time / fraction_of_max_velocity

        # Gotten using math; Makes the player stop in the amount of time 'self.running_deceleration_time'
        self.deceleration_path.acceleration = (-self.deceleration_path.initial_velocity)/time_needed

        self.deceleration_path.start()
        self.deceleration_path.max_time = time_needed

    def player_movement_direction_is_same_as_deceleration(self):
        """returns: boolean; if the direction the player is moving is equal to the deceleration"""

        deceleration_direction_is_rightwards = self.deceleration_path.acceleration < 0
        return ((deceleration_direction_is_rightwards and key_is_hit(self.right_key)) or
                not deceleration_direction_is_rightwards and key_is_hit(self.left_key))

    def set_current_velocity(self):
        """returns: double; the current velocity of the player"""

        deceleration_has_not_finished = self.deceleration_path.current_time > 0
        if deceleration_has_not_finished:
            current_velocity = self.deceleration_path.get_velocity_using_time(self.deceleration_path.current_time)
            # Figuring out the time to get to that velocity, so the player can continue to accelerate to the max velocity
            self.acceleration_path.start()
            self.acceleration_path.current_time = sqrt(abs(current_velocity) / self.acceleration_path.acceleration)

        GameMovement.run_acceleration(self, key_is_hit(self.left_key) or key_is_hit(self.right_key), self.acceleration_path)

    def can_decelerate(self):
        """returns: boolean; if the player can decelerate (they couldn't if an object was in the way"""

        deceleration_direction_is_rightwards = self.deceleration_path.acceleration < 0
        return self.can_move_right if deceleration_direction_is_rightwards else self.can_move_left

    def run_bottom_collision(self, y_coordinate):
        """Runs what should happen after a bottom collision (the player should rebound off of it)"""

        velocity = self.jumping_path.get_velocity_using_displacement(self.jumping_path.initial_distance + y_coordinate)
        self.jumping_path.set_variables(initial_velocity=velocity)
        self.jumping_path.reset()
        self.y_coordinate = y_coordinate

    def get_velocity(self):
        """returns: double; the current velocity of the player"""

        return_value = None
        if self.deceleration_path.has_finished():
            return_value = self.current_velocity

        else:
            return_value = self.deceleration_path.get_velocity_using_time(self.deceleration_path.current_time)

        return return_value

    # Collision Stuff
    def run_inanimate_object_collision(self, inanimate_object, index_of_sub_component, time):
        """Runs what should happen when the player collides with an inanimate object"""

        if index_of_sub_component == self.index_of_user:
            self.update_platform_collision_data(inanimate_object, time)

        if index_of_sub_component != self.index_of_user:
            self.weapon.run_inanimate_object_collision(inanimate_object, index_of_sub_component - self.weapon_index_offset, time)

    def run_collisions(self, time):
        """Runs what should happen based on what got stored in the collision data"""

        # The player should only act upon the collision data if there was stuff in the History Keeper because if there wasn't
        # Then the game is automatically going to say it was not a collision (top, left, right, bottom)
        if HistoryKeeper.get_last_from_time(self.name, time) is not None:
            self.alter_player_horizontal_movement()
            self.alter_player_vertical_movement()

    def alter_player_horizontal_movement(self):
        """Alters the player's horizontal movement so it stays within the screen and is not touching the platforms"""

        player_is_beyond_screen_left = self.x_coordinate <= 0
        player_is_beyond_screen_right = self.right_edge >= screen_length

        self.can_move_left = not self.right_collision_data[0] and not player_is_beyond_screen_left
        self.can_move_right = not self.left_collision_data[0] and not player_is_beyond_screen_right

        # Setting the player's x coordinate if the any of the above conditions were met (collided with platform or beyond screen)
        function = self.set_x_coordinate
        self.change_attribute_if(player_is_beyond_screen_left, function, 0)
        self.change_attribute_if(player_is_beyond_screen_right, function, screen_length - self.length)

        if self.right_collision_data[0]:
            function(self.right_collision_data[1].right_edge)

        if self.left_collision_data[0]:
            function(self.left_collision_data[1].x_coordinate - self.length)

    def alter_player_vertical_movement(self):
        """Alters the player's vertical movement so it can't go through platforms"""

        player_is_on_platform = self.top_collision_data[0]

        if player_is_on_platform:
            self.set_y_coordinate(self.top_collision_data[1].y_coordinate - self.height)
            self.gravity_engine.game_object_to_physics_path[self].reset()

        self.set_is_on_platform(player_is_on_platform)

        if self.bottom_collision_data[0]:
            self.gravity_engine.game_object_to_physics_path[self].reset()
            self.run_bottom_collision(self.bottom_collision_data[1].bottom)

    def render(self):
        """Renders the object onto the screen"""

        eye_color = (0, 0, 255)
        mouth_color = red

        eye1 = Segment(
            color=eye_color,
            percent_down=20,
            percent_right=25,
            percent_length=20,
            percent_height=20)

        eye2 = Segment(
            color=eye_color,
            percent_down=eye1.percent_down,
            percent_right=eye1.right_edge + 10,
            percent_length=eye1.percent_length,
            percent_height=eye1.percent_height)

        mouth = Segment(
            color=mouth_color,
            percent_down=60,
            percent_right=10,
            percent_length=80,
            percent_height=10)

        self.draw_in_segments([eye1, eye2, mouth])

    @property
    def is_beyond_screen_left(self):
        self.x_coordinate <= 0

    @property
    def is_beyond_screen_right(self):
        self.right_edge >= screen_length

    def change_attribute_if(self, condition, function, value):
        """Changes the attribute to the value if 'condition()' is True"""

        if condition:
            function(value)

    # TODO change me back
    def cause_damage(self, amount):
        """Damages the player by that amount and also starts the player's invincibility"""

        if self.invincibility_event.has_finished():
            self.hit_points_left -= amount
            self.invincibility_event.start()
