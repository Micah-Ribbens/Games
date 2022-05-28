from base.quadratic_equations import PhysicsPath


class GravityEngine:
    """Runs all the gravity for the objects"""

    game_objects = []
    physics_paths = []

    def __init__(self, game_objects, time, acceleration_displacement):
        """Initializes the object"""

        self.game_objects = game_objects

        for x in range(len(self.game_objects)):
            physics_path = PhysicsPath()
            physics_path.set_acceleration(time, acceleration_displacement)
            self.physics_paths.append(physics_path)

    def run(self):
        """Runs all the gravity code"""

        for x in range(len(self.game_objects)):
            game_object = self.game_objects[x]
            physics_path: PhysicsPath = self.physics_paths[x]

            # if game_object.is_on_platform:
            #     print("STOP")
            physics_path.run(game_object.is_on_platform, not game_object.is_on_platform)

            game_object.y_coordinate += physics_path.get_distance_from_acceleration()

    def reset(self):
        """Resets everything back to the start of the game"""

        for physics_path in self.physics_paths:
            physics_path.reset()