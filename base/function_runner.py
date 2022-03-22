from base.utility_classes import HistoryKeeper


class FunctionRunner:
    """Provides a way to run functions automatically"""

    events = {}
    timed_events = {}
    functions = {}
    tracked_objects = []

    def __int__(self):
        self.events = {}
        self.timed_events = {}
        self.functions = {}
        self.tracked_objects = []

    def add_event(self, event, function):
        """ summary: adds the event to events, so the event's run function will be run every cycle

            params:
                event: Event; the event that will be added to events
                function: Function; will be used like this 'event.run(function())'

            returns: None
        """

        self.events[event] = function

    def add_timed_event(self, timed_event, reset_event, start_event):
        """ summary: adds the timed_event to timed_events, so the timed_events's run function will be run every cycle

            params:
                event: Event; the event that will be added to events
                reset_event: Function; will be used like this 'timed_event.run(reset_event(), start_event())'
                start_event: Function; will be used like this 'timed_event.run(reset_event(), start_event())'

            returns: None
        """

        self.timed_events[timed_event] = [reset_event, start_event]

    def run_if(self, function, condition):
        """Runs the function if the condition is True"""

        if condition:
            function()

    def run_until(self, function, condition):
        """ summary: runs the function until condition() is False

            params:
                function: Function; the function that will be run
                condition: Function; the condition that will stop the function from running

            returns: None
        """

        self.functions[function] = condition

    def track_game_object(self, game_object):
        """Keeps track of the game_object so it will be added to HistoryKeeper every cycle"""

        self.tracked_objects.append(game_object)

    def run(self):
        """Runs all the functions and adds all the tracked objects to the HistoryKeeper"""

        for event in self.events.keys():
            function = self.events.get(event)
            event.run(function())

        for timed_event in self.timed_events.keys():
            reset_event, start_event = self.timed_events.get(timed_event)
            timed_event.run(reset_event(), start_event())

        for function in self.functions.keys():
            condition = self.functions.get(function)

            if not condition():
                self.functions.pop(function)

            else:
                function()

        for tracked_object in self.tracked_objects:
            HistoryKeeper.add(tracked_object, id(tracked_object), True)
