from base.quadratic_equations import PhysicsPath


class GravityEngine:
    """Runs all the gravity for the objects"""

    game_object_to_physics_path = {}

    def __init__(self, game_objects, acceleration):
        """Initializes the object"""

        for game_object in game_objects:
            physics_path = PhysicsPath()
            physics_path.acceleration = acceleration
            self.game_object_to_physics_path[game_object] = physics_path

    def run(self):
        """Runs all the gravity code"""

        for game_object in self.game_object_to_physics_path.keys():
            physics_path: PhysicsPath = self.game_object_to_physics_path[game_object]

            physics_path.run(game_object.is_on_platform, not game_object.is_on_platform)

            game_object.y_coordinate += physics_path.get_gravity_distance_from_acceleration()

    def reset(self):
        """Resets everything back to the start of the game"""

        for physics_path in self.game_object_to_physics_path.values():
            return physics_path.reset()
