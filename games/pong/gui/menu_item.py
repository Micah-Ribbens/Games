from gui_components.text_box import TextBox
from base.events import TimedEvent
from base.colors import *
from base.important_variables import *


class MenuItem(TextBox):
    """The items that the alter sizes screen use"""
    
    values = []
    label = ""
    properties_modifying = []
    button_events = {}
    # Important Note: This class doesn't modify this property; the AlterSizesScreen does
    # I did this because the menu_item(s) are unselected if another item gets clicked
    is_selected = True
    increase_by = 0

    def __init__(self, label, default_values, properties_modifying, increase_by):
        """ summary: initializes the object 
            
            params: 
                label: String; the name that is displayed for the menu item
                default_values: List of int; the values that are displayed originally after the label
                properties_modifying: List of String; the properties that this object modifies
                increase_by: int; how much a click of the button increases the values
            
            returns: None
        """
        
        self.properties_modifying = properties_modifying
        self.label = label
        self.values = default_values
        self.increase_by = increase_by

        # Text is assigned in the render method
        super().__init__("", 15, False, white, blue)

    def render(self):
        """ summary: renders the item on the screen
            params: None
            returns: None
        """
        
        self.text = (f"{self.label}: ({self.values[0]}, {self.values[1]})" if self.values.__len__() == 2
                     else f"{self.label}: {self.values[0]}")

        TextBox.render(self)

    def instantiate_needed_objects(self, key):
        """ summary: instantiates the event for the key if it already doesn't exist
            
            params:
                key: int; the value of the key that should be instantiated
            
            returns: None
        """
        
        if not self.button_events.__contains__(f"held in{key}"):
            self.button_events[f"held in{key}"] = TimedEvent(1, False)

        if not self.button_events.__contains__(f"held increase{key}"):
            self.button_events[f"held increase{key}"] = TimedEvent(.1, True)

    def can_change_value(self, key, is_subtracting, value, key_click_event):
        """ summary: finds out if the values of this object should be increased
            
            params:
                key: int; the key that is used to change the value
                is_subtracting: boolean; if the value being changed is negative
                value: int; the amount that the value will be changed by
                key_click_event: Event; the keys click event
            
            returns: boolean; if the value can be changed
        """
        
        controls = pygame.key.get_pressed()

        self.instantiate_needed_objects(key)

        key_is_held_in_event: TimedEvent = self.button_events.get(f"held in{key}")
        held_in_increase_event: TimedEvent = self.button_events.get(f"held increase{key}")

        reset_event = not controls[key]
        key_is_held_in_event.run(reset_event, controls[key])
        # If the key is held in then the held in increase event should run otherwise it shouldn't
        held_in_increase_event.run(reset_event, key_is_held_in_event.is_done())

        is_click = not key_click_event.happened_last_cycle() and controls[key]

        if is_subtracting and value - self.increase_by <= 0:
            return False

        return self.is_selected and (is_click or held_in_increase_event.is_done())

    def do_multiple_value_logic(self, left_key_event, right_key_event):
        """ summary: does the logic for changing the values if this object modifies multiple values

            params:
                left_key_event: Event; the event for the left key
                right_key_event: Event; the event for the right key

            returns: None
        """

        controls = pygame.key.get_pressed()

        if self.can_change_value(pygame.K_LEFT, True, self.values[1], left_key_event) and controls[pygame.K_LEFT]:
            self.values[1] -= self.increase_by

        if self.can_change_value(pygame.K_RIGHT, False, self.values[1], right_key_event) and controls[pygame.K_RIGHT]:
            self.values[1] += self.increase_by

    def run(self, up_key_event, down_key_event, left_key_event, right_key_event):
        """ summary: runs the logic for adding and subtracting values

            params:
                up_key_event: Event; the event for the up key
                down_key_event: Event; the event for the down key
                left_key_event: Event; the event for the left key
                right_key_event: Event; the event for the right key
        """

        controls = pygame.key.get_pressed()

        # IMPORTANT NOTE: self.can_change_value() must be first in the if statement followed by controls[key]
        # Otherwise the pause between holding the key down and repeatedly adding values doesn't work
        if self.can_change_value(pygame.K_UP, False, self.values[0], up_key_event) and controls[pygame.K_UP]:
            self.values[0] += self.increase_by

        if self.can_change_value(pygame.K_DOWN, True, self.values[0], down_key_event) and controls[pygame.K_DOWN]:
            self.values[0] -= self.increase_by

        # Some menu items can alter multiple values, but others don't
        has_multiple_values = len(self.values) == 2

        if has_multiple_values:
            self.do_multiple_value_logic(left_key_event, right_key_event)
