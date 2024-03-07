from pyglet.window import key as Key
from pyglet.window import mouse as Mouse


class Controller:
    # general controls
    pause = "pause"
    close = "close"

    click = "click"

    # game controls
    up, down, left, right = "up", "down", "left", "right"

    def __init__(self, window):
        self.window = window

        self.mouse_position = (0, 0)
        self.text = ""  # text written by player during frame

        self.control_to_key_set = dict()    # Keybind states
        self.key_to_control = dict()    # n key to 1 control mapping

        # define inputs (should be read from a file)
        self.control_to_key_set[Controller.up] = {Key.UP}
        self.control_to_key_set[Controller.down] = {Key.DOWN}
        self.control_to_key_set[Controller.left] = {Key.LEFT}
        self.control_to_key_set[Controller.right] = {Key.RIGHT}
        self.control_to_key_set[Controller.click] = {Mouse.LEFT}

        # fill key_to_control
        for ctrl in self.control_to_key_set:
            for key in self.control_to_key_set[ctrl]:
                self.key_to_control[key] = ctrl

        # controls states (tracks numbers of keys pressing control)
        self.control_held_down = dict()
        self.control_pressed = dict()
        # fill
        for ctrl in self.control_to_key_set:
            self.control_held_down[ctrl] = 0
            self.control_pressed[ctrl] = 0

        @self.window.event
        def on_key_press(symbol, modifiers=None):
            control = self.get_control(symbol)
            if control:  # False if unused key
                self.press_control(control)

        @self.window.event
        def on_key_release(symbol, modifiers=None):
            control = self.get_control(symbol)
            if control:  # False if unused key
                self.release_control(control)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            on_key_press(button, modifiers)
            self.reset_control(self.pause)

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            on_key_release(button, modifiers)

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.mouse_position = (x, y)

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.mouse_position = (x, y)

        @self.window.event
        def on_text(text):
            self.text += text

        @self.window.event
        def on_activate():
            self.reset_control(self.pause)

        @self.window.event
        def on_deactivate():
            # reset control state because inputs are no longer tracked until activated again
            self.reset()
            self.press_control(self.pause)

        @self.window.event
        def on_close():
            self.press_control(self.close)

        # Other possible actions: on_mouse_[action]
        # enter, leave, scroll, drag

        @self.window.event
        def on_move(x, y):
            self.reset()
            self.press_control(self.pause)

    def get_control(self, key):
        return self.key_to_control.get(key, False)

    def get_text(self):
        return self.text

    def get_key_set(self, control):
        return self.control_to_key_set.get(control, False)

    def update(self, dt):
        pass

    def update_reset(self):
        self.text = ""
        for control in self.control_pressed:
            self.control_pressed[control] = 0

    def reset(self):
        self.update_reset()
        for control in self.control_held_down:
            self.reset_control(control)

    def press_control(self, control):
        self.control_held_down[control] = self.control_held_down.get(control, 0) + 1
        self.control_pressed[control] = 1

    def release_control(self, control):
        self.control_held_down[control] = max(0, self.control_held_down.get(control, 0) - 1)

    def reset_control(self, control):
        self.control_held_down[control] = 0
        self.control_pressed[control] = 0

    def is_control_pressed(self, control):
        return self.control_pressed.get(control, 0) > 0

    def is_control_held_down(self, control):
        return self.control_held_down.get(control, 0) > 0
