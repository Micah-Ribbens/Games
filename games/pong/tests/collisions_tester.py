import pygame.key

from base_pong.dimensions import Dimensions
from base_pong.events import Event
from base_pong.important_variables import screen_length, screen_height
from base_pong.path import ObjectPath
from gui_components.graph import Graph
from gui_components.grid import Grid
from gui_components.screen import Screen
from gui_components.text_box import TextBox
from base_pong.colors import *


class FailedCase:
    want = False
    got = False
    case_type = ""
    case_number = ""
    object1_path: ObjectPath = None
    object2_path: ObjectPath = None

    def __init__(self, want, got, case_type, case_number, object1_path, object2_path):
        self.want, self.got = want, got
        self.case_type, self.case_number = case_type, case_number
        self.object1_path, self.object2_path = object1_path, object2_path


class CollisionsTester(Screen):
    current_screen = None
    screens = []
    screen_number = 0
    left_clicked_event = Event()
    right_clicked_event = Event()

    def __init__(self, failed_cases):
        for failed_case in failed_cases:
            if failed_case.case_type == "Path":
                self.screens.append(self.get_path_case_screen(failed_case))
            else:
                self.screens.append(self.get_moving_screen(failed_case))

        self.current_screen = self.screens[0]

    def get_components(self):
        return [] if self.current_screen is None else self.current_screen.get_components()

    def get_path_case_screen(self, failed_case):
        """returns: Screen; the screen that would display everything for a path collision"""

        screen = Screen()
        top_bar_components = [TextBox(f"Wanted: {failed_case.want}", 15, False, purple, white),
                              TextBox(f"Got: {failed_case.got}", 15, False, green, white),
                              TextBox(f"Path Test #{failed_case.case_number}", 15, False, black, white)]
        top_grid = Grid(Dimensions(0, 0, screen_length, screen_height * .1), None, 1, True)
        top_grid.turn_into_grid(top_bar_components, None, None)


        x_line1, right_edge_line1, y_line1, bottom_line1 = failed_case.object1_path.get_time_lines()
        x_line2, right_edge_line2, y_line2, bottom_line2 = failed_case.object2_path.get_time_lines()
        graphs = [
            # X Graphs
            Graph([x_line1, x_line2, right_edge_line2], [red, purple, purple]),
            Graph([right_edge_line1, x_line2, right_edge_line2], [red, purple, purple]),
            Graph([x_line2, x_line1, right_edge_line1], [red, purple, purple]),
            Graph([right_edge_line2, x_line1, right_edge_line1], [red, purple, purple]),

            # Y Graphs
            Graph([y_line1, y_line2, bottom_line2], [red, purple, purple]),
            Graph([bottom_line1, y_line2, bottom_line2], [red, purple, purple]),
            Graph([y_line2, y_line1, bottom_line1], [red, purple, purple]),
            Graph([bottom_line2, y_line1, bottom_line1], [red, purple, purple]),
        ]
        buffer = screen_height * .02
        graph_grid = Grid(Dimensions(0, top_grid.dimensions.bottom + buffer, screen_length, screen_height - top_grid.dimensions.height - buffer), None, 2, True)
        graph_grid.turn_into_grid(graphs, graph_grid.dimensions.length / 4, graph_grid.dimensions.height / 4)

        screen.components = graphs + top_bar_components
        return screen

    def get_moving_screen(self, failed_case: FailedCase):
        """returns: Screen; the screen that would display everything for only one object moving"""

        screen = Screen()
        top_bar_components = [TextBox(f"Wanted: {failed_case.want}", 15, False, purple, white),
                              TextBox(f"Got: {failed_case.got}", 15, False, green, white),
                              TextBox(f"Moving Test #{failed_case.case_number}", 15, False, black, white)]
        top_grid = Grid(Dimensions(0, 0, screen_length, screen_height * .1), None, 1, True)
        top_grid.turn_into_grid(top_bar_components, None, None)

        object1_is_moving = failed_case.object1_path.get_total_distance() == 0

        if object1_is_moving:
            screen.components = self.get_moving_components(failed_case.object1_path, failed_case.object2_path.current_object) + top_bar_components
        else:
            screen.components = self.get_moving_components(failed_case.object2_path, failed_case.object2_path.current_object) + top_bar_components

        return screen

    def run(self):
        """Runs everything in order for this screen to work properly"""

        controls = pygame.key.get_pressed()


        if not self.left_clicked_event.happened_last_cycle() and controls[pygame.K_LEFT]:
            self.screen_number -= 1

        if not self.left_clicked_event.happened_last_cycle() and controls[pygame.K_RIGHT]:
            self.screen_number -= 1

    def get_moving_components(self, moving_object_path: ObjectPath, stationary_object):
        """returns: List of Component; the components scaled to fit the screen"""

        screen_x_middle = screen_length / 2
        screen_y_middle = screen_length / 2
        max_length = screen_length / 3
        max_height = screen_height / 3

        # screen_x_middle / (moving_object_path.get_x_distance()
        min_x = min(moving_object_path.prev_object.x_coordinate, moving_object_path.current_object.x_coordinate, stationary_object.x_coordinate)
        max_x = max(moving_object_path.prev_object.right_edge, moving_object_path.current_object.right_edge, stationary_object.right_edge)

        min_y = min(moving_object_path.prev_object.y_coordinate, moving_object_path.current_object.y_coordinate, stationary_object.y_coordinate)
        max_y = max(moving_object_path.prev_object.bottom, moving_object_path.current_object.bottom, stationary_object.bottom)

        x_units = max_length / (max_x - min_x)
        y_units = max_height / (max_y - min_y)

        moving_object_path.path_line.start_point.x_coordinate = screen_x_middle + (x_units * moving_object_path.path_line.start_point.x_coordinate)
        moving_object_path.path_line.end_point.x_coordinate = screen_x_middle + (x_units * moving_object_path.path_line.end_point.x_coordinate)
        moving_object_path.path_line.start_point.y_coordinate = screen_y_middle + (y_units * moving_object_path.path_line.start_point.y_coordinate)
        moving_object_path.path_line.end_point.y_coordinate = screen_y_middle + (y_units * moving_object_path.path_line.end_point.y_coordinate)

        stationary_object.x_coordinate = screen_x_middle + (x_units * stationary_object.x_coordinate)
        stationary_object.length = x_units * stationary_object.length
        stationary_object.y_coordinate = screen_y_middle + (y_units * stationary_object.y_coordinate)
        stationary_object.height = y_units * stationary_object.height

        return [moving_object_path, stationary_object]















