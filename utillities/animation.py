from base.utility_classes import Range
from base.velocity_calculator import VelocityCalculator


class Animation:
    """Allows animations to be run"""

    max_time = 0
    components = []
    colors = []
    ranges = []
    function = []
    current_time = 0
    is_done = True
    is_running = False
    prev_index = -1

    def __init__(self, times):
        """Initializes the object"""

        current_time = 0

        for time in times:
            self.ranges.append(Range(current_time, current_time + time))
            current_time += time

        self.max_time = current_time

    def run_animation(self, components, colors, function):
        """Runs the actions for the amount of times from __init__() """

        self.components, self.colors = components, colors
        self.function = function
        self.is_running = True
        self.is_done = False
        self.current_time = 0

    def run(self):
        """Runs all the code necessary for this object to work"""

        for x in range(len(self.ranges)):
            if self.is_running and self.ranges[x].__contains__(self.current_time):
                self.function(self.components[x], self.colors[x])

        self.current_time += VelocityCalculator.time
        if self.current_time > self.max_time:
            self.is_running = False
            self.is_done = True



