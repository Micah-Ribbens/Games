from base.important_variables import game_window, screen_length, screen_height, background_color
from base.utility_functions import validate_kwargs_has_all_fields


def render_words(message, font, **kwargs):
    """ summary: draws words onto the screen; either x_coordinate, y_coordinate, and text_is_center
        must be provided or is_center_of_screen

        params:
            x_coordinate: int; the x_coordinate of the text
            y_coordinate: int; the y_coordinate of the text
            is_center: boolean; the x and y coordinates are the center of the text (if True) otherwise start of text
            is_center_of_screen: boolean; the text is in the center of the screen
            text_color (optional): tuple; the (Red, Green, Blue) values of text color; is (255, 255, 255) if not specified
            text_background (optional) tuple; the (Red, Green, Blue) values of the background of the text; is background_color if not specified

        returns: None
    """

    # Getting all the variables
    text_color = (255, 255, 255) if not kwargs.get("text_color") else kwargs.get("text_color")
    text_background = background_color if not kwargs.get("text_background") else kwargs.get("text_background")
    is_center_of_screen = False if not kwargs.get("is_center_of_screen") else kwargs.get("is_center_of_screen")
    is_center = False if not kwargs.get("is_center") else kwargs.get("is_center")
    text = font.render(message, True, text_color, text_background)
    text_rect = text.get_rect()

    if is_center_of_screen:
        text_rect.center = (screen_length / 2, screen_height / 2)

    else:
        validate_kwargs_has_all_fields(["x_coordinate", "y_coordinate"], kwargs)
        text_rect.left = kwargs.get("x_coordinate")
        text_rect.top = kwargs.get("y_coordinate")

    if is_center:
        text_rect.center = (kwargs.get("x_coordinate"), kwargs.get("y_coordinate"))

    game_window.get_window().blit(text, text_rect)