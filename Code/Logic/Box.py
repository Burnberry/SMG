from Code.Util.GameObject import GameVisualObject
from Code.Util.Assets import Img, Alpha


class Box(GameVisualObject):
    def __init__(self, position):
        super().__init__(position, Img.BoxOpen)

        self.x, y = position
        self.highlighted = None
        self.default = Img.BoxOpen
        self.crossed = Img.BoxCrossed

    def update(self, dt):
        pass

    def set_assets(self, default=None, crossed=None):
        if default:
            self.default = default
        if crossed:
            self.crossed = crossed

    def open(self):
        self.asset = self.default

    def cross(self):
        self.asset = self.crossed

    def inside(self, cx, cy):
        return self.visual.inside(cx, cy)

    def highlight(self, on):
        if self.highlighted != on:
            self.highlighted = on
            self._highlight(on)

    def _highlight(self, on):
        if on:
            color = (255, 255, 127)
        else:
            color = (255, 255, 255)
        self.visual.set_color(color)


class Digit(GameVisualObject):
    def __init__(self, position, digit):
        asset = Alpha.SymbolDict[digit]
        super().__init__(position, asset)

        self.x, y = position

    def update(self, dt):
        pass

    def set_digit(self, digit):
        self.asset = Alpha.SymbolDict[digit]

    def inside(self, cx, cy):
        return self.visual.inside(cx, cy)

    def set_visibility(self, visible=True):
        self.visual.set_visibility(visible)
