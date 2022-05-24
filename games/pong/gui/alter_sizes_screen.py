import pygame

from gui_components.grid import Grid
from base.utility_functions import percentages_to_numbers, change_attributes
from games.pong.gui.menu_item import MenuItem
from games.pong.base_pong.players import Player
from games.pong.base_pong.ball import Ball
from base.important_variables import *
from base.velocity_calculator import VelocityCalculator
from base.dimensions import Dimensions
from base.events import Event
from gui_components.sub_screen import SubScreen
from base.utility_functions import key_is_hit


# Paddle Dimension and Ball Dimensions
class AlterSizesScreen(SubScreen):
    """The screen that allows the user to alter the sizes of the paddle and ball"""

    paddle = Player()
    paddle1 = Player()
    paddle2 = Player()
    up_key_event = None
    down_key_event = None
    left_key_event = None
    right_key_event = None
    ball = Ball()
    menus = None
    name = "Alter Sizes"
    game_screen = None

    def __init__(self, length_used_up, height_used_up, game_screen):
        """ summary: initializes the AlterSizesScreen

            params:
                length_used_up: int; the length that is used up by the main screen (this is a sub screen)
                height_used_up: int; the height that is used by the main screen (this is a sub screen)
                game_screen: int; the screen where the game is run (actual Pong part)

            returns: None
        """
        self.paddle2, self.paddle1 = game_screen.player2, game_screen.player1
        self.paddle2.x_coordinate = screen_length - self.paddle2.length
        paddle_y_coordinate = height_used_up
        self.paddle1.y_coordinate, self.paddle2.y_coordinate = paddle_y_coordinate, paddle_y_coordinate
        self.game_screen = game_screen

        self.ball.reset()

        self.down_key_event = Event()
        self.left_key_event = Event()
        self.right_key_event = Event()
        self.up_key_event = Event()

        function_runner.add_event(self.up_key_event, lambda: key_is_hit(pygame.K_UP))
        function_runner.add_event(self.down_key_event, lambda: key_is_hit(pygame.K_DOWN))
        function_runner.add_event(self.right_key_event, lambda: key_is_hit(pygame.K_RIGHT))
        function_runner.add_event(self.left_key_event, lambda: key_is_hit(pygame.K_LEFT))

        self.menus = [MenuItem("Paddle Dimensions", [Player().height, Player().length], ["height", "length"], 5),
                      MenuItem("Ball Dimensions", [Ball().height, Ball().length], ["height", "length"], 5),
                      MenuItem("Paddle Power", [Player().power], ["power"], .25),
                      MenuItem("Ball Speed", [Ball().base_forwards_velocity], ["base_velocity"],
                               int(VelocityCalculator.give_velocity(screen_length, 2)))]

        self.components = self.menus

        self.components = [self.ball, self.paddle1, self.paddle2]
        for menu in self.menus:
            menu.is_runnable = False
            self.components.append(menu)
        x_coordinate, y_coordinate, length, height = percentages_to_numbers(
            0, 0, 100, 100, screen_length, screen_height)

        grid = Grid(Dimensions(x_coordinate, y_coordinate,
                    length, height), 2, None, False)

        max_height = VelocityCalculator.give_measurement(screen_height, 10)
        grid.turn_into_grid(self.menus, None, max_height)

    def do_menu_item_logic(self):
        """ summary: runs all the menu item logic (each menu item modifies a certain attribute like ball size)
            params: None
            returns: None
        """
        controls = pygame.key.get_pressed()



        for menu_item in self.menus:
            if menu_item.got_clicked():
                self.reset_is_selected()
                menu_item.is_selected = True

            menu_item.run(self.up_key_event, self.down_key_event,
                          self.left_key_event, self.right_key_event)

    def run(self):
        """ summary: runs all the necessary logic in order for the alter sizes screen to work
            params: None
            returns: None
        """
        self.do_menu_item_logic()
        self.change_attributes()

    def reset_is_selected(self):
        """ summary: makes menu items is_selected property set to false
            params: None
            returns: None
        """

        for menu_item in self.menus:
            menu_item.is_selected = False

    def change_attributes(self):
        """ summary: changes game screen's player1 and player2's attributes to reflect what was altered in the alter sizes screen
            params: None
            returns: None
        """
        # Alters the attributes for the objects that will change the attributes down below
        for menu in self.menus:
            object_modifying = self.paddle if menu.label.__contains__("Paddle") else self.ball
            object_modifying.__dict__[menu.properties_modifying[0]] = menu.values[0]

            if menu.properties_modifying.__len__() == 2:
                object_modifying.__dict__[menu.properties_modifying[1]] = menu.values[1]

        # Changes all the attributes to reflect what was stored in the objects above
        change_attributes(self.game_screen.player1, self.paddle, ["length", "height", "power"])
        change_attributes(self.game_screen.player2, self.paddle, ["length", "height", "power"])
        self.game_screen.player2.x_coordinate = screen_length - self.paddle2.length
        change_attributes(self.game_screen.ball, self.ball, ["base_velocity", "length", "height"])

    def render(self):
        pass
