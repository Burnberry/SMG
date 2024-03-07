from abc import ABC, abstractmethod
from pyglet.sprite import Sprite
from Code.Util.GameObject import GameVisualObject
from Code.Util.Assets import Alpha
from Code.Util.CustomAssets import CustomAssetGen
from Code.Util.SettingsGlobal import SettingsGlobal


class VisualClass(ABC):
    @abstractmethod
    def update_visual(self, obj, camera):
        pass

    @abstractmethod
    def remove(self):
        pass


class VisualClassUI(ABC):
    @abstractmethod
    def remove(self):
        pass


def get_anchor_offsets(anchor, w, h):
    x_offset, y_offset = 0, 0
    ax, ay = anchor[1], anchor[0]
    if ax == 'c':
        x_offset = -w//2
    elif ax == 'r':
        x_offset = -(w-1)

    if ay == 'c':
        y_offset = -h//2
    elif ay == 't':
        y_offset = -(h-1)

    return x_offset, y_offset


class VisualImage(VisualClass):
    def __init__(self, asset, batch, group=None, anchor="bl"):
        self.anchor = anchor
        self.asset = asset
        self.sprite = Sprite(asset.get(), batch=batch, group=group)
        self.sprite.update(scale=SettingsGlobal.Scale)

    def update_visual(self, obj: GameVisualObject, camera):
        if obj.asset != self.asset:
            self.asset.release()
            self.asset = obj.asset
            self.sprite.image = self.asset.get()

        x, y = obj.get_position()
        self.move_sprite(x, y, camera)

    def move_sprite(self, x, y, camera):
        w, h = self.get_onscreen_dimensions()
        dx, dy = get_anchor_offsets(self.anchor, w, h)
        cx, cy = camera.to_screen_coords(x, y)
        self.sprite.update(x=cx+dx, y=cy+dy)

    def update_image(self, asset):
        self.sprite.image = asset.get()

    def set_visibility(self, visible=True):
        self.sprite.visible = visible

    def set_color(self, color):
        self.sprite.color = color

    def set_screen_position(self, cx, cy):
        w, h = self.get_onscreen_dimensions()
        dx, dy = get_anchor_offsets(self.anchor, w, h)
        self.sprite.update(x=cx+dx, y=cy+dy)

    def get_onscreen_dimensions(self):
        return self.sprite.width, self.sprite.height

    def get_onscreen_position(self):
        return self.sprite.x, self.sprite.y

    def inside(self, cx, cy):
        w, h = self.get_onscreen_dimensions()
        x, y = self.get_onscreen_position()
        return (x <= cx < x + w) and (y <= cy < y + h)

    def remove(self):
        self.asset.release()
        self.sprite.delete()


class UIBox(VisualClassUI):
    def __init__(self, cx, cy, w, h, batch, group=None, anchor="bl"):
        self.cx, self.cy, self.w, self.h, self.anchor = cx, cy, w, h, anchor
        self.highlighted = None
        self.color = (255, 255, 255)

        data = self.generate_data()
        img = CustomAssetGen.generate(data, w, h)
        self.sprite = Sprite(img, x=cx, y=cy, batch=batch, group=group)
        self.sprite.update(scale=SettingsGlobal.Scale)

        w, h = self.get_onscreen_dimensions()
        self.x_offset, self.y_offset = get_anchor_offsets(self.anchor, w, h)
        self.set_position(self.cx, self.cy)

    def set_position(self, cx, cy):
        self.cx, self.cy = cx, cy
        cx, cy = cx + self.x_offset, cy + self.y_offset
        self.sprite.update(x=cx, y=cy)

    def set_color(self, color):
        self.color = color
        self.update_color()

    def update_color(self):
        if self.highlighted:
            return
        self.sprite.color = self.color

    def set_anchor(self, anchor):
        self.anchor = anchor
        w, h = self.get_onscreen_dimensions()
        self.x_offset, self.y_offset = get_anchor_offsets(self.anchor, w, h)
        self.set_position(self.cx, self.cy)

    def resize_element(self, w, h):
        self.w, self.h = w, h
        self.x_offset, self.y_offset = get_anchor_offsets(self.anchor, self.w, self.h)
        data = self.generate_data()
        img = CustomAssetGen.generate(data, self.w, self.h)
        self.sprite.image = img

        w, h = self.get_onscreen_dimensions()
        self.x_offset, self.y_offset = get_anchor_offsets(self.anchor, w, h)
        self.set_position(self.cx, self.cy)

    def generate_data(self):
        data, pixel_inner, pixel_outer = b'', b'', b''
        # RGBA
        for i in [255, 255, 255, 255]:
            pixel_outer += i.to_bytes(1, 'big')
        for i in [255, 255, 255, 127]:
            pixel_inner += i.to_bytes(1, 'big')

        if self.w < 2 or self.h < 2:
            print("UIbox width/height is too small to make box / VisualClass")
            return

        edge = pixel_outer*self.w
        inner = pixel_outer + pixel_inner*(self.w-2) + pixel_outer

        data = edge + inner*(self.h-2) + edge

        return data

    def get_onscreen_dimensions(self):
        scale = SettingsGlobal.Scale
        w, h = self.w, self.h
        return w*scale, h*scale

    def get_onscreen_position(self):
        return self.cx + self.x_offset, self.cy + self.y_offset

    def remove(self):
        self.sprite.delete()

    def inside(self, cx, cy):
        w, h = self.get_onscreen_dimensions()
        cx1, cy1 = self.get_onscreen_position()
        return (cx1 <= cx < cx1 + w) and (cy1 <= cy < cy1 + h)

    def highlight(self, on=True):
        if self.highlighted != on:
            self.highlighted = on
            self._highlight()

    def _highlight(self):
        if self.highlighted:
            self.sprite.color = (255, 255, 127)
        self.update_color()


def make_text(lines, batch, group):
    """
    :return:
    :letters: list of VisualImages of letters
    :spacings: list of distances between symbols (start positions)
    :height
    """
    letters, spacings, height, width = [], [], 0, 0
    default_space_x, default_space_y = 1, 1
    space_spacing = 3
    x_spacing, y_spacing = 0, 0
    height0, width0 = 0, 0

    for line in lines[::-1]:
        for symbol in line:
            if symbol == ' ':
                x_spacing += space_spacing
                continue

            asset = Alpha.get(symbol)
            if asset is None:
                continue

            letters.append(VisualImage(asset, batch, group))
            spacing = (x_spacing, y_spacing)
            spacings.append(spacing)

            w, h = asset.get_dimensions()
            height0 = max(h, height0)
            x_spacing += default_space_x + w
        x_spacing -= default_space_x
        width = max(x_spacing, width)
        x_spacing = 0
        y_spacing += height0 + default_space_y
    height = y_spacing - default_space_y

    return letters, spacings, width, height


class UITextBox(UIBox):
    def __init__(self, cx, cy, text, batch, group_ui=None, group_text=None, anchor="bl"):
        self.text = self._to_text(text)

        self.cx, self.cy = cx, cy
        self.batch, self.group_text = batch, group_text
        self.exterior_width, self.exterior_height = 2, 2

        self.lines, self.text_spacings, self.text_width, self.text_height = make_text(self.text, batch, group_text)
        w, h = self.text_width + 2*self.exterior_width, self.text_height + 2*self.exterior_height
        super().__init__(cx, cy, w, h, batch, group=group_ui, anchor=anchor)

        self.set_position(cx, cy)

    @staticmethod
    def _to_text(text):
        if type(text) is str:
            return [text]
        else:
            return text

    def set_position(self, cx, cy):
        super().set_position(cx, cy)
        scale = SettingsGlobal.Scale

        cx += self.x_offset + scale*self.exterior_width
        cy += self.y_offset + scale*self.exterior_height
        for i in range(len(self.lines)):
            visual = self.lines[i]
            dx, dy = self.text_spacings[i]
            dx *= scale
            dy *= scale
            visual.set_screen_position(cx+dx, cy+dy)

    def set_text(self, text):
        self.text = self._to_text(text)
        self.lines, self.text_spacings, self.text_width, self.text_height = make_text(self.text, self.batch, self.group_text)
        w, h = self.text_width + 2 * self.exterior_width, self.text_height + 2 * self.exterior_height
        super().resize_element(w, h)

        self.set_position(self.cx, self.cy)

    def remove(self):
        self.remove_text()
        super().remove()

    def remove_text(self):
        for visual in self.lines:
            visual.remove()
