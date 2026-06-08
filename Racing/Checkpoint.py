import arcade

class Checkpoint:
    def __init__(self, pixels: set, rect: arcade.Rect, index: int, colour: tuple, world_height: int):
        self.pixels = pixels
        self.rect = rect
        self.index = index
        self.colour = colour
        self.passed = False

    def contains_mask(self, px, py):
        return (px, py) in self.pixels