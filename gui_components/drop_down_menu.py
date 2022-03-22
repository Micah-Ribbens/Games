from gui_components.clickable_component import ClickableComponent
from gui_components.text_box import TextBox
from base.drawable_objects import GameObject
from base.colors import *
from base.important_variables import *
from base.utility_functions import percentages_to_numbers


class DropDownMenu(ClickableComponent):
    """A menu that can be expanded and unexpanded"""

    items = []
    portions = []
    text_color = None
    background_color = None
    font_size = 0
    is_expanded = False
    title = ""
    text = ""
    selected_item = ""
    # This is the part of the drop down menu that is supposed to be clicked
    clickable_component = None
    prev_time = 0

    def get_selected_item(self):
        """ summary: gets the selected item from the drop down menu and returns it
            params: None
            returns: String; the drop down menu's selected item
        """

        return self.selected_item

    def add_item(self, text):
        """ summary: adds the item to the drop down menu

            params:
                text; String; the text of the item

            returns: None
        """

        item = TextBox(text, self.font_size, False,
                       self.text_color, self.background_color)

        self.items.append(item)

    def __init__(self, title, item_names, text_color, background_color, font_size, selected_index):
        """ summary: initializes the object

            params:
                title: String; the title of the drop down menu
                item_names; List of String; the names of the items that the drop down menu will display
                text_color: tuple; the (Red, Green, Blue) values of the text
                background_color: tuple; the (Red, Green, Blue) values of the drop down menu's background
                font_size: int; the size of the text
                selected_index: int; the index of the initial item that is selected

            returns: None
        """

        # Makes it so each drop down's menu items are unique
        self.items = []
        self.prev_time = 0
        self.text_color = text_color
        self.background_color = background_color
        self.font_size = font_size
        self.title = title
        # This sets the text that is selected automatically without the user's input
        self.text = item_names[selected_index]
        self.selected_item = item_names[selected_index]

        for item_name in item_names:
            self.add_item(item_name)

        ClickableComponent.__init__(self)

    def run(self):
        """ summary: runs the expansion and un expansion logic of the drop down menu
            params: None
            returns: None
        """

        # The code below alters is_expanded, so this stores this value
        was_expanded = self.is_expanded

        if self.got_clicked() or self.an_item_got_clicked():
            # Makes it so collapses when expanded and expands when collapsed
            self.is_expanded = not self.is_expanded

        for item in self.items:
            # Once the DropDownMenu is expanded an item can be clicked during that same click
            # So this prevents the top item being selected automatically
            if item.got_clicked() and was_expanded:
                self.text = item.text
                self.selected_item = item.text
            item.run()

        # clickable_component isn't set in run, so if the other function isn't called before run then
        # the clickable_component could be None
        if self.clickable_component is not None:
            self.clickable_component.run()

    def get_title_portion(self):
        """ summary: creates a title portion of the drop down menu then returns it
            params: None
            returns: TextBox; the title portion of the drop down menu
        """

        title_portion = TextBox(self.title, self.font_size, False, self.text_color, background_color)
        title_portion.number_set_dimensions(self.x_coordinate, self.y_coordinate, self.length, self.height)

        return title_portion

    def render(self):
        """ summary: renders the drop down menu
            params: None
            returns: None
        """

        title_portion = self.get_title_portion()
        last_item = title_portion
        # Divided into two sections; the text portion and the arrow showing portion
        text_portion_length = self.length * .9
        text_portion = TextBox(
            self.text, self.font_size, False, self.text_color, self.background_color)

        text_portion.number_set_dimensions(
            self.x_coordinate, last_item.bottom, text_portion_length, self.height)

        # So it doesn't reset the clickable component every cycle making it impossible to tell if the component got clicked
        if self.clickable_component is None:
            self.clickable_component = ClickableComponent()
            self.clickable_component.number_set_dimensions(self.x_coordinate, last_item.bottom, self.length, self.height)

        # Creates a divider between the text and the arrow
        divider_length = self.length * .02
        divider = GameObject(text_portion.right_edge, last_item.bottom,
                             self.height, divider_length, white)

        used_up_length = divider_length + text_portion_length

        remaining_length = self.length - used_up_length

        text_portion.render()
        divider.render()
        self.render_arrow_portion(
            remaining_length, divider.right_edge, last_item.bottom)

        if self.is_expanded:
            self.render_items(last_item)

    def render_arrow_portion(self, remaining_length, x_coordinate, y_coordinate):
        """ summary: renders the arrow portion of the drop down menu
            params: None
            returns: None
        """

        arrow_container = GameObject(x_coordinate, y_coordinate,
                                     self.height, remaining_length, self.background_color)

        # From here down is talking about the arrow part
        percent_down = 20
        percent_right = 20

        # The offset percent_down and percent_right should be equal on both sides
        # Thats what the code below does
        percent_length = 100 - (percent_right * 2)
        percent_height = 100 - (percent_down * 2)

        arrow_numbers = percentages_to_numbers(
            percent_right, percent_down, percent_length, percent_height, remaining_length, self.height)
        # number_to_right and number_downwards is how much right and how much down it should be in relation to the component
        number_to_right, number_downwards, length, height = arrow_numbers

        # The arrow is right after the divider
        start_x_coordinate = number_to_right + x_coordinate
        start_y_coordinate = number_downwards + y_coordinate

        # End x coordinate and y coordinate meaning the bottom point of the triangle
        end_y_coordinate = start_y_coordinate + height
        # This would be the halfway point of the vertices of the top of the triangle
        end_x_coordinate = start_x_coordinate + (length // 2)

        # arrow_container must be render before the arrow, so the arrow can render on top of the arrow_container
        arrow_container.render()
        pygame.draw.polygon(game_window.get_window(), white,
                            [(start_x_coordinate, start_y_coordinate), (start_x_coordinate + length, start_y_coordinate), (end_x_coordinate, end_y_coordinate)])

    def render_items(self, last_item):
        """ summary: renders the items of the drop down menu (only called if expanded)

            params:
                last_item: Component; the item that each item in the drop down menu will be placed below

            returns: None
        """

        for item in self.items:
            buffer_between_items = self.get_buffer_between_items(last_item)
            item.number_set_dimensions(self.x_coordinate, buffer_between_items.bottom, self.length, self.height)
            buffer_between_items.render()
            item.render()

            last_item = item

    def get_buffer_between_items(self, last_item):
        """ summary: creates a buffer that will be used between the items then returns it

            params:
                last_item: Component; the item that the buffer will be placed directly below

            returns: GameObject; the buffer between the items
        """

        return GameObject(last_item.x_coordinate, last_item.bottom, last_item.height * .1, last_item.length, white)

    def an_item_got_clicked(self):
        """ summary: iterates over each item in items to check if it got clicked
            params: None
            returns: boolean; if an item in items got clicked
        """

        is_clicked = False
        for item in self.items:
            if item.got_clicked():
                is_clicked = True

        return is_clicked

    def got_clicked(self):
        """ summary: finds out if the clickable component of the drop down menu got clicked
            params: None
            returns: boolean; if the drop down menu got clicked
        """

        # The clickable component is set during the first cycle making it impossible to be clicked if it isn't set yet
        is_clicked = False if self.clickable_component is None else self.clickable_component.got_clicked()

        return is_clicked
