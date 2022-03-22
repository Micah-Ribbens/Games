class VelocityCalculator:
    """Stores the time of the last run cycle and gives functionality for calculating velocities and measurements"""
    # As in the time it took for there to be one iteration
    time = 0

    def give_velocity(unit_of_measurement, how_many_units):
        """ summary: Figures out the velocity by multiplying 1/1000 of unit_of_measurement by how_many_units

            params:
                unit_of_measurement: int; is what how_many_units is multiplied by (screen_length and screen_height are recommended)
                how_many_units: int; how many units of the unit_of_measurement

            returns: int; the velocity that was gotten by multiplying unit_of_measurement / 1000 by how_many_units
        """
        return (unit_of_measurement / 1000) * how_many_units

    def calc_distance(velocity):
        """ summary: calculates the distance the velocity has traveled the last cycle (velocity * time last cycle took)

            params:
                velocity: int; the velocity of the object (will be multiplied by the time last cycle took)

            returns: the distance that the object traveled with that velocity
        """
        return VelocityCalculator.time * velocity

    def give_measurement(unit_of_measurement, how_many_units):
        """summary: Figures out the measurement by multiplying 1/100 of unit_of_measurement by how_many_units

            params:
                unit_of_measurement: int; is what how_many_units is multiplied by (screen_length and screen_height are recommended)
                how_many_units: int; how many units of the unit_of_measurement

            returns: int; the measurement that was gotten by multiplying unit_of_measurement / 1000 by how_many_units"""
        return (unit_of_measurement / 100) * how_many_units

