from pygame import mixer
import pygame
from base.velocity_calculator import VelocityCalculator

mixer.init()
pygame.init()


class SoundEffect:
    """A class for playing sound effects"""

    sound_effect = None
    is_playing = False
    max_time = 0
    current_time = 0
    sound_name = ""

    def __init__(self, sound_name, max_time):
        """Initializes the object"""

        self.sound_effect = mixer.Sound(sound_name)
        self.max_time = max_time
        self.sound_name = sound_name

    def play(self):
        """Plays the sound effect for the given amount of time"""

        self.is_playing = True
        self.sound_effect.play()
        print("PLAY")

    def stop(self):
        """Stops playing the sound effect"""

        self.is_playing = False
        self.sound_effect.stop()

    def run(self):
        """Runs all the code necessary for using this class"""

        if self.is_playing:
            self.current_time += VelocityCalculator.time

        if self.current_time > self.max_time:
            self.stop()
            self.current_time = 0



