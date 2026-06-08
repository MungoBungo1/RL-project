import arcade
import math

class FinishLine(arcade.Sprite):
    def __init__(self, image_file: str, scale: float):
        super().__init__(image_file, scale)

    def is_crossed(self, car: arcade.Sprite) -> bool:
        # Simple bounding box collision detection
        return arcade.check_for_collision(self, car)