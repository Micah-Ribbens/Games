# TODO make sure to add the new generated platforms and maybe other stuff to the History Keeper, so collisions can happen
import random

from base.equations import Point
from base.important_variables import screen_height, screen_length
from base.path import SimplePath
from base.velocity_calculator import VelocityCalculator
from games.platformers.base.platform import Platform
from games.platformers.base.player import Player


class Generator:
    """Generates platforms, enemies, and other things semi-randomly (as long as it is playable for the player and mantains a good difficulty)"""

    # Modifiable Numbers
    max_y_change = VelocityCalculator.give_measurement(screen_height, 25)
    min_platform_height = int(VelocityCalculator.give_measurement(screen_height, 10))
    max_platform_height = int(VelocityCalculator.give_measurement(screen_height, 20))
    min_platform_length = int(VelocityCalculator.give_measurement(screen_length, 15))
    max_platform_length = int(VelocityCalculator.give_measurement(screen_length, 25))
    length_multiplier = 1.5
    min_distance_accuracy_decrease = .05

    def generate_platform(self, player: Player, last_platform, difficulty):
        """returns: Platform; the next platform, which would be after 'last_platform;' uses the difficulty to decide how hard of a jump it should be"""

        accuracy = self._get_accuracy(difficulty)
        new_platform_height = random.randint(self.min_platform_height, self.max_platform_height)

        topmost_y_coordinate = player.get_topmost_y_coordinate(last_platform, accuracy, self._get_accuracy(1))
        bottommost_y_coordinate = self._get_bottommost_y_coordinate(last_platform, new_platform_height)
        new_platform_y_coordinate = random.randint(topmost_y_coordinate, bottommost_y_coordinate)

        new_platform_length = random.randint(self.min_platform_length, self.max_platform_length)

        max_vertical_time = player.get_max_time_to_y_coordinate(last_platform.y_coordinate, new_platform_y_coordinate)

        max_distance = self.get_horizontal_distance(max_vertical_time, player, accuracy)
        min_distance = self.get_horizontal_distance(max_vertical_time, player, accuracy - self.min_distance_accuracy_decrease)
        distance = random.randint(min_distance, max_distance)

        new_platform_x_coordinate = last_platform.right_edge + distance
        if new_platform_x_coordinate + new_platform_length > screen_length:
            new_platform_x_coordinate = screen_length - new_platform_x_coordinate

        return Platform(new_platform_x_coordinate, new_platform_y_coordinate, new_platform_length, new_platform_height, True)

    def get_horizontal_distance(self, vertical_time, player, accuracy):
        """returns: double; the horizontal distance apart the old platform and the new one should be"""

        # 2 * player's length because one of them comes from the player not being affected by gravity until its
        # x coordinate > the last platform's right edge and other one because they can land on the new platform when
        # the right edge is > the new platform's x coordinate
        return vertical_time * player.max_velocity * accuracy + player.length * 2

    def get_hardest_platform(self, player: Player, last_platform, difficulty):
        """returns: Platform; the hardest platform possible at this difficulty"""

        accuracy = self._get_accuracy(difficulty)
        platform_height = random.randint(self.min_platform_height, self.max_platform_height)

        platform_y_coordinate = player.get_topmost_y_coordinate(last_platform, accuracy, self._get_accuracy(1))

        platform_length = random.randint(self.min_platform_length, self.max_platform_length)

        max_vertical_time = player.get_max_time_to_y_coordinate(last_platform.y_coordinate, platform_y_coordinate) * accuracy

        # 2 * player's length because one of them comes from the player not being affected by gravity until its
        # x coordinate > the last platform's right edge and other one because they can land on the new platform when
        # the right edge is > the new platform's x coordinate
        platform_x_coordinate = last_platform.right_edge + self.get_horizontal_distance(max_vertical_time, player, accuracy)

        if platform_x_coordinate + platform_length > screen_length:
            platform_x_coordinate = screen_length - platform_length

        return Platform(platform_x_coordinate, platform_y_coordinate, platform_length, platform_height, True)

    def get_easiest_platform(self, player: Player, last_platform, difficulty):
        """returns: Platform; the easiest platform possible at this difficulty"""

        accuracy = self._get_accuracy(difficulty)
        platform_height = random.randint(self.min_platform_height, self.max_platform_height)
        platform_y_coordinate = self._get_bottommost_y_coordinate(last_platform, platform_height)

        platform_length = random.randint(self.min_platform_length, self.max_platform_length)

        max_vertical_time = player.get_max_time_to_y_coordinate(last_platform.y_coordinate, platform_y_coordinate)
        platform_x_coordinate = last_platform.right_edge + self.get_horizontal_distance(max_vertical_time, player, accuracy)

        if platform_x_coordinate + platform_length > screen_length:
            platform_x_coordinate = screen_length - platform_length

        return Platform(platform_x_coordinate, platform_y_coordinate, platform_length, platform_height, True)

    def _get_accuracy(self, difficulty):
        """returns: double; how accurate the player has to be (1 - margin_of_error)"""

        margins_of_error = SimplePath(Point(0, 35))
        margins_of_error.add_point(Point(20, 30))
        margins_of_error.add_point(Point(40, 25))
        margins_of_error.add_point(Point(60, 20))
        margins_of_error.add_point(Point(70, 15))
        margins_of_error.add_point(Point(80, 10))
        margins_of_error.add_point(Point(90, 6))
        margins_of_error.add_point(Point(100, 3))

        # Margins_of_error are in percentages
        return 1 - ( margins_of_error.get_y_coordinate(difficulty) / 100 )

    def _get_bottommost_y_coordinate(self, last_platform, platform_height):
        """returns: double; the generated platform's bottommost y_coordinate (must stay within the screen)"""

        return_value = last_platform.y_coordinate + self.max_y_change

        # The platform's bottom must be visible
        if return_value + platform_height >= screen_height:
            return_value = screen_height - platform_height

        return return_value




