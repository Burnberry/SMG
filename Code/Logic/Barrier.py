from Code.Util.GameObject import GameVisualObject
from Code.Util.Assets import Img


class Barrier(GameVisualObject):
    def __init__(self, position):
        super().__init__(position, Img.Barrier)

        self.x, y = position

    def update(self, dt):
        pass
