from pyglet import graphics
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.VisualClass import VisualImage, UIBox, UITextBox


class Renderer:
    Background = graphics.Group(order=SettingsGlobal.GroupOrderBackground)
    Foreground = graphics.Group(order=SettingsGlobal.GroupOrderForeground)
    Foreground2 = graphics.Group(order=SettingsGlobal.GroupOrderForeground+1)
    UI = graphics.Group(order=SettingsGlobal.GroupOrderUI)
    Text = graphics.Group(order=SettingsGlobal.GroupOrderText)

    def __init__(self, window, camera):
        self.window = window
        self.camera = camera
        self.batch = graphics.Batch()
        self.object_dict = dict()
        self.UI_elements = set()

    def draw(self):
        self.window.clear()
        self.update_objects()
        self.batch.draw()
        self.window.flip()

    def clear(self):
        for element in list(self.UI_elements):
            self.remove_ui_element(element)

        for obj in list(self.object_dict):
            self.remove_obj(obj)

    def signal_associate_removal(self, obj):
        self.remove_obj(obj)

    def remove_obj(self, obj):
        if obj not in self.object_dict:
            return
        for visual in self.object_dict.pop(obj):
            visual.remove()

    def remove_ui_element(self, element):
        if element in self.UI_elements:
            self.UI_elements.remove(element)
            element.remove()

    def update_objects(self):
        for obj in self.object_dict:
            for visual in self.object_dict[obj]:
                visual.update_visual(obj, self.camera)

    def add_object(self, obj):
        if obj not in self.object_dict:
            self.object_dict[obj] = set()

    def add_visual(self, obj, visual):
        self.add_object(obj)
        self.object_dict[obj].add(visual)

    def add_ui_visual(self, visual):
        self.UI_elements.add(visual)

    def make_visual_image(self, obj, group=None, anchor="bl"):
        visual = VisualImage(obj.asset, self.batch, group, anchor)
        obj.set_visual(visual)
        obj.add_associate(self)
        visual.update_visual(obj, self.camera)
        self.add_visual(obj, visual)
        return visual

    # unfinished
    def make_ui_visual(self, x, y, asset, group=None, anchor="bl"):
        ui_visual = VisualImage(asset, self.batch, group, anchor)
        ui_visual.set_screen_position(x, y)
        self.add_ui_visual(ui_visual)
        return ui_visual

    def make_ui_box(self, x, y, w, h, group=None, anchor="bl"):
        ui_box = UIBox(x, y, w, h, self.batch, group, anchor)
        self.add_ui_visual(ui_box)
        return ui_box

    def make_ui_text_box(self, x, y, text, group_ui=None, group_text=None, anchor="bl"):
        ui_box = UITextBox(x, y, text, self.batch, group_ui, group_text, anchor)
        self.add_ui_visual(ui_box)
        return ui_box
