from base.utility_functions import get_kwarg_item



class QuadraticEquation:
    """A class that defines the necessary variables for a quadratic ax^2 + bx + c"""
    h = 0
    k = 0
    a = 0

    def set_variables(self, h, k, a):
        """ summary: sets the variables to the numbers to equation: a(x-h)^2 + k

            params:
                h: double; the first number of the vertex
                k: double; the second number of the vertex
                a: double; the number that goes before (x-h)^2

            returns: None
        """

        self.h = h
        self.k = k
        self.a = a

    def get_number(self, x):
        """ summary: finds the number by plugging x into the equation ax^2 + bx + c

            params:
                x: double; the variable x that will be used to get the number

            returns: double; the number that is gotten when x is plugged into the equation
        """

        return self.a * pow((x - self.h), 2) + self.k

    def points_set_variables(self, vertex, other_point):
        """ summary: sets the variables based on both points

            params:
                vertex: Point; the vertex of the quadratic equation
                other_point: Point; another point besides the vertex

            returns: None
        """

        self.h = vertex.x_coordinate
        self.k = vertex.y_coordinate
        other_point.y_coordinate = other_point.y_coordinate

        # Figured this out using algebra
        self.a = (other_point.y_coordinate - self.k) / pow((other_point.x_coordinate - self.h), 2)


class PhysicsEquation:
    """A class that uses common physics equations for initial_velocity, acceleration, and initial_distance"""
    acceleration = 0
    initial_velocity = 0
    initial_distance = 0

    def get_time_to_vertex(self):
        """ summary: gets the time it takes to reach the vertex knowing that the final initial_velocity is 0, so the time is -initial_velocity / acceleration
            params: None
            returns: double; the time to reach the vertex
        """

        return -self.initial_velocity / self.acceleration

    def set_acceleration(self, time, displacement):
        """ summary: sets the acceleration knowing that d = 1/2 * a * t^2 where d is displacement, a is acceleration, and t is time

            params:
                time_to_fall: double; the amount of time that it should take to go that amount (displacement)
                time: double; the distance (up being positive and down being negative) that it should travel

            returns: None
        """

        self.acceleration = (2 * displacement) / pow(time, 2)

    def set_velocity(self, vertex, time):
        """ summary: sets the velocity of knowing that d = vit + 1/2at^2 + di
                     IMPORTANT: initial_distance and acceleration must be set prior to this being called

            params:
                vertex: double; the highest/lowest point of the parabola
                time: double; the time it takes to get to the vertex

            returns: None
        """
        self.initial_velocity = (vertex - self.initial_distance) / time - self.acceleration * time * 1 / 2

    def set_all_variables(self, vertex, time, acceleration_displacement, initial_distance):
        """ summary: sets all the variables; calls set_velocity and set_acceleration

            params:
                vertex: double; the highest/lowest point of the parabola
                time: double; the time it takes to get to the vertex/go the acceleration_distance
                acceleration_displacement: double; the distance (up being positive and down being negative) that the acceleration in that time
                initial_distance: double; the initial distance

            returns: None
        """

        self.initial_distance = initial_distance
        self.set_acceleration(time, acceleration_displacement)
        self.set_velocity(vertex, time)

    def set_variables(self, **kwargs):
        """ summary: sets the variables to the number provided

            params:
                acceleration: double; the acceleration (can be positive or negative) | a in 1/2 * ax^2 + bx + c
                initial_velocity: double; the initial_velocity (can be positive or negative) | b in 1/2 * ax^2 + bx + c
                initial_distance: double; the starting point (can be positive or negative) | c in 1/2 * ax^2 + bx + c

            returns: None
        """

        self.acceleration = get_kwarg_item(kwargs, "acceleration", self.acceleration)
        self.initial_velocity = get_kwarg_item(kwargs, "initial_velocity", self.initial_velocity)
        self.initial_distance = get_kwarg_item(kwargs, "initial_distance", self.initial_distance)

    def get_distance(self, time):
        """ summary: finds the number by plugging x into the equation 1/2 * at^2 + vt + d
                     where a is acceleration, t is time, v is initial_velocity, and d is initial_distance

            params:
                time: double; the amount of time that has passed

            returns: double; the number that is gotten when time is plugged into the equation
        """
        return 1 / 2 * self.acceleration * pow(time, 2) + self.initial_velocity * time + self.initial_distance

    def get_velocity_using_time(self, time):
        """ summary: uses the fact that the initial_velocity is equal to vi - at^2 where vi is the initial initial_velocity, a is acceleration, and t is time
                     to find the initial_velocity

            params:
                time: double; the amount of time that the initial_velocity has been affected by acceleration

            returns: double; the initial_velocity after affected by acceleration
        """

        return self.initial_velocity + self.acceleration * time

    def get_velocity_using_displacement(self, displacement):
        """ summary: uses the formula vf^2 = vi^2 + 2ax to find the initial_velocity
                     where vf is final initial_velocity, vi is initial initial_velocity, a is acceleration, and x is displacement

            params:
                displacement: double; the amount that the ball has traveled (upwards is positive and downwards is negative)

            returns: double; the final initial_velocity
        """

        final_velocity_squared = pow(self.initial_velocity, 2) + 2 * self.acceleration * displacement
        # Reduces the risk of a rounding error like -1*e^-15 would cause an imaginary number exception
        return pow(int(final_velocity_squared), 1 / 2)