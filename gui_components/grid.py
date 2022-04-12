from math import ceil, floor
from base.velocity_calculator import VelocityCalculator
from base.important_variables import *
from base.dimensions import Dimensions


class Grid:
    """Provides an easy way to put components into a grid"""
    dimensions: Dimensions = 0
    max_columns = 0
    max_rows = 0
    starts_at_top = False
    number_of_items = 0
    length_buffer = VelocityCalculator.give_measurement(screen_length, 1)
    height_buffer = VelocityCalculator.give_measurement(screen_height, 1)

    # function takes instantiates the values of the instances of the grid 
    def __init__(self, dimensions, max_columns, max_rows, starts_at_top):
        """ summary: initializes the object | IMPORTANT - max_columns and max_rows can't both be None

            params:
                dimensions: Dimensions; the x_coordinate, y_coordinate, length, and height of the grid
                max_columns: int; the max amount of columns the grid can have (can be None)
                max_rows: int; the max amount of rows the grid can have (can be None)
                starts_at_top: boolean; if the components of the grid start at the top (start at bottom if False)

            returns: None
        """

        self.dimensions = dimensions
        self.max_columns, self.max_rows = max_columns, max_rows
        self.starts_at_top = starts_at_top

        if max_columns is None and max_rows is None:
            raise ValueError("Max columns or max rows must have a value; they both can't be None")

    def turn_into_grid(self, items, item_max_length: int, item_max_height: int):
        """ summary: turns all the items into a grid format

            params:
                items: List of Component; the items that will be converted into a grid
                item_max_length: int; the max length that an item can be
                item_max_height: int; the max height than an item can be

            returns: None
        """

        self.number_of_items = len(items)

        # If there are no items, then nothing can be turned into a grid
        if self.number_of_items == 0:
            return

        rows = self.get_rows()
        columns = self.get_columns()
        item_length = self.get_item_length(columns, item_max_length)
        item_height = self.get_item_height(rows, item_max_height)
        base_y_coordinate = self.dimensions.y_coordinate if self.starts_at_top else self.dimensions.bottom - item_height

        for x in range(self.number_of_items):
            # Both would start at 0 (0 is the first column and row)
            column_number = x % columns
            row_number = floor(x / columns)
            # Multiplying row_number by item_height because each row that is done increases the y_coordinate that a item should be at
            # For instance, if it is at the 2nd row then one item was before it so it'd be row_number * item_height
            y_coordinate_change = row_number * item_height if self.starts_at_top else -(row_number * item_height)

            # The row and column numbers are multiplied by the buffers to add the neccessary buffers. For instance, if it is in column 3
            # The item in column 1 and column 2 had a buffer, so it'd be the length_buffer * 2
            change_from_height_buffer = (row_number * self.height_buffer) if self.starts_at_top else -(row_number * self.height_buffer)
            change_from_length_buffer = (column_number * self.length_buffer)

            y_coordinate_change += change_from_height_buffer

            # Multiplying column_number by item_length because each column that is before it increases the x_coordinate that a item should be at
            # For instance, if it is at the 2nd column then one item was before it so it'd be column_number * item_length
            x_coordinate = (column_number * item_length) + change_from_length_buffer + self.dimensions.x_coordinate
            y_coordinate = base_y_coordinate + y_coordinate_change

            items[x].number_set_dimensions(x_coordinate, y_coordinate, item_length, item_height)

    def get_item_length(self, columns, item_max_length):
        """ summary: divides the available length by the number of columns to figure out each item's length in the grid

            params:
                columns: int; the number of columns that the grid has
                item_max_length: int; the max length of an item

            returns: int; the length that each item in the grid should be
        """

        # Must minus the length buffer * (number_of_items - 2) from the regular length because
        # Every item has the length_buffer after it besides the first and last item, so hence the minus 2
        remaining_length = self.dimensions.length - (self.length_buffer * (columns - 2))

        length = remaining_length // columns

        if item_max_length is not None and length > item_max_length:
            length = item_max_length
        
        return length

    def get_item_height(self, rows, item_max_height):
        """ summary: divides the available height by the number of rows to calculate each item's height in the grid

            params:
                rows: int; the amount of rows in the grid
                item_max_height: int; the max height of the items in the grid

            returns: int; the height of each item in the grid
        """

        # Must minus the height_buffer * (number_of_items - 2) from the regular height because
        # Every item has the self.height_buffer after it besides the first and last item, so hence the minus 2
        remaining_height = self.dimensions.height - (self.height_buffer * (self.number_of_items - 2))
        height = remaining_height // rows

        if item_max_height is not None and height > item_max_height:
            height = item_max_height
        
        return height

    def get_columns(self):
        """ summary: finds the number of columns by dividing the number of items by the number of rows
            params: None
            returns: int; the number of columns in the grid
        """

        rows = self.max_rows if self.max_rows is not None else self.get_rows()

        # The overfill of number_of_items / max_rows must be an additional column
        # For instance if they are 5 items and there are 2 rows there must be 3 columns
        columns = ceil(self.number_of_items / rows)

        if self.max_columns is not None and columns > self.max_columns:
            columns = self.max_columns
        
        return columns
    
    def get_rows(self):
        """ summary: finds the number of rows by dividing the number of items by the number of columns
            params: None
            returns: int; the number of rows in the grid
        """

        columns = self.max_columns if self.max_columns is not None else self.get_columns()
        # The overfill of number_of_items / max_columns must be an additional row
        # For instance if they are 5 items and there are 2 columns there must be 3 rows.
        rows = ceil(self.number_of_items / columns)

        if self.max_rows is not None and rows > self.max_rows:
            rows = self.max_rows
        
        return rows