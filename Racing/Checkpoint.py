import arcade

class Checkpoint:
    def __init__(self, rect: arcade.Rect, index: int):
        self.rect = rect
        self.index = index
        self.passed = False

    def contains(self, x, y):
        return self.rect.contains(x, y)