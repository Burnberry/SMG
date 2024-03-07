import math

from Code.Util.GameObject import GameObject


class TestMovingBox(GameObject):
    def __init__(self, position):
        super().__init__()

        self.center = position
        self.time_passed = 0
        self.radius = 50

    def update(self, dt):
        self.time_passed += dt

        x, y = self.center

        x += math.cos(self.time_passed)*self.radius
        y += math.sin(self.time_passed)*self.radius
        self.position = (x, y)
