import arcade
import math

class Car(arcade.Sprite):
    def __init__(self, image_file: str, scale: float):
        super().__init__(image_file, scale)

    def Accelerate(self, amount: float):
        radians = math.radians(self.angle)

        self.change_x += math.cos(radians) * amount
        self.change_y -= math.sin(radians) * amount

    def Decelerate(self, amount: float):
        radians = math.radians(self.angle)

        self.change_x -= math.cos(radians) * amount
        self.change_y += math.sin(radians) * amount

    def apply_drag(self, factor: float):
        self.change_x *= factor
        self.change_y *= factor

        if abs(self.change_x) < 0.01:
            self.change_x = 0
        if abs(self.change_y) < 0.01:
            self.change_y = 0

    def Rotate(self, angle: float):
        self.angle += angle