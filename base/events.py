from base.utility_classes import HistoryKeeper, Range
from base.velocity_calculator import VelocityCalculator


class Event:
    """Used to store an event from the current cycle and past cycles (event being anything that is a boolean)"""

    name = None

    def __init__(self):
        self.name = id(self)

    def is_continuous(self, event):
        """summary: uses HistoryKeeper.get_last() to get the event from the last cycle to check if the event is continuous
            
            params: 
                event: boolean; the event from the current cycle
            
            returns: boolean; if the event from the previous cycle is True and the event from the current cycle is True
        """

        return HistoryKeeper.get_last(self.name) and event

    def run(self, event):
        """
            summary: uses HistoryKeeper.add() to store the event for the current cycle, which will be accessed by is_continuous()
            params:
                event: boolean; the event from the current cycle
            returns: None
        """
        HistoryKeeper.add(event, self.name, False)

    def happened_last_cycle(self):
        """ summary: uses HistoryKeeper.get_last() to get the event from the last cycle and see if it is True

            params: None

            returns: boolean; if the event was True last cycle
        """

        return HistoryKeeper.get_last(self.name)


class TimedEvent:
    """Used for events that are completed within a certain time frame"""
    time_needed = 0
    is_started = False
    restarts_upon_completion = False
    current_time = 0

    def __init__(self, time_needed, restarts_upon_completion):
        """ summary: initializes the object by modifying the attributes with the values provided
            
            params:
                time_needed: int; the time it takes for the TimedEvent to end
                restarts_upon_completion: boolean; if the TimedEvent automatically restarts if the time_needed is surpassed
            
            returns: None
        """

        self.time_needed = time_needed
        self.restarts_upon_completion = restarts_upon_completion

    def is_done(self):
        """ summary: Figures out if the current_time that has passed is greater than or equal the time_needed to pass
            params: None
            returns: boolean; if the TimedEvent is done (current_time >= time_needed)
        """

        is_finished = self.is_started

        if self.current_time < self.time_needed:
            is_finished = False

        if is_finished and self.restarts_upon_completion:
            self.start()
            self.current_time = 0

        return is_finished

    def run(self, reset_event, start_event):
        """ summary: if the reset_event is True then the TimedEvent resets and if the start_event is True then it starts
            If the TimedEvent is_started then the current_time increases by the time it took the current cycle to run

            params: 
                reset_event: boolean; the event that if True resets the current_time to 0 and stops the TimedEvent
                start_event: boolean; the event that if True starts the TimedEvent
            
            returns: None
        """

        if reset_event:
            self.reset()

        elif start_event:
            self.start()

        if self.is_started:
            self.current_time += VelocityCalculator.time

    def start(self):
        """ summary: Should be treated as private; starts the TimedEvent (sets is_started to True)
            params: None
            returns: None
        """

        self.is_started = True

    def reset(self):
        """" summary: Should be treated as private: resets the TimedEvent (sets is_started to False and the current_time to 0)
            params: None
            returns: None
        """

        self.is_started = False
        self.current_time = 0


class TimedRange:
    """Used for events that do different things at different times"""

    ranges = []
    current_time = 0

    def __init__(self, times):
        """ summary: initializes the object

            params:
                times: double; the length of each range of time; range goes from previous range end -> time + previous range end

            returns: None
        """

        current_time = 0
        for time in times:
            self.ranges.append(Range(current_time, current_time + time))
            current_time += time

    def run(self):
        """Runs all the code necessary for the TimedRange to work"""

        self.current_time += VelocityCalculator.time

    def reset(self):
        """Resets the TimedRange back to its start"""
        self.current_time = 0

    def get_current_index(self):
        """returns: int; the index that the TimedRange is currently at"""

        return_value = len(self.ranges) - 1
        for x in range(self.ranges):
            if self.ranges[x].__contains__(self.current_time):
                return_value = x

        return return_value

    def is_done(self):
        """returns: boolean; if the TimedRange has completed"""

        last_range = self.ranges[len(self.ranges) - 1]
        return self.current_time > last_range.end


