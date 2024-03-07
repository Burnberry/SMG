from pyglet import clock
from pyglet.window import Window
from Code.Util.SystemStuff import SystemStuff
from Code.Util.Camera import Camera
from Code.Util.Controller import Controller
from Code.Util.Renderer import Renderer
from Code.Util.GameObject import GameObject
from Code.Logic.MainScene import MainScene
from Code.Logic.Levels import *


class Game:
    def __init__(self):
        self.tick = 0
        self.run = False
        self.dt = 0
        self.time = 0

        # Camera/window stuff
        x, y = 0, 0
        res_w, res_h = 16*24, 9*24
        w, h = SystemStuff.get_screen_resolution()
        if not SettingsGlobal.Fullscreen:
            SettingsGlobal.Scale = min(7*w//(res_w*8), 7*h//(res_h*8))
        else:
            SettingsGlobal.Scale = min(w // res_w, h // res_h)
        width, height = res_w*SettingsGlobal.Scale, res_h*SettingsGlobal.Scale
        self.camera = Camera(x, y, width, height, SettingsGlobal.Scale)

        caption = SettingsGlobal.GameName
        if SettingsGlobal.Fullscreen:
            self.window = Window(fullscreen=SettingsGlobal.Fullscreen, caption=caption)
        else:
            self.window = Window(width=width, height=height, caption=caption)

        # Renderer
        self.renderer = Renderer(self.window, self.camera)

        # Setup controller
        self.controller = Controller(self.window)

        # Scene
        self.scene = MainScene(self)

    def start(self):
        self.run = True
        while self.run:
            # Wait for frame and handle inputs
            self.dt = clock.tick()
            self.handle_input()

            if self.controller.is_control_pressed(Controller.pause):
                continue

            self.time += self.dt
            self.scene.update(self.dt)
            self.handle_scene()
            GameObject.update_active_objects(self.dt)
            self.renderer.draw()

            self.controller.update_reset()
            self.tick += 1

        self.end()

    def handle_input(self):
        self.dispatch_events()
        self.controller.update(self.dt)

        if self.controller.is_control_pressed(Controller.close):
            self.run = False
            return

        if self.controller.is_control_pressed(Controller.pause):
            self.controller.update_reset()
            return

    def handle_scene(self):
        if not self.scene.switchState:
            return

        if self.scene.switchState == "L0":
            self.renderer.clear()
            self.scene = Level0(self)

        if self.scene.switchState == "L1":
            self.renderer.clear()
            self.scene = Level1(self)

        if self.scene.switchState == "L2":
            self.renderer.clear()
            self.scene = Level2(self)

        if self.scene.switchState == "L3":
            self.renderer.clear()
            self.scene = Level3(self)

        if self.scene.switchState == "L4":
            self.renderer.clear()
            self.scene = LevelB(self)

        if self.scene.switchState == "L5":
            self.renderer.clear()
            self.scene = LevelF(self)

        if self.scene.switchState == "CONTINUE":
            self.renderer.clear()
            self.scene = MainScene(self)

        if self.scene.switchState == "BACK":
            self.renderer.clear()
            self.scene = MainScene(self)

        if self.scene.switchState == "START":
            self.renderer.clear()
            self.scene = Level0(self)

    def end(self):
        pass

    def close(self):
        self.window.close()

    def dispatch_events(self):
        return self.window.dispatch_events()

    def clear(self):
        self.window.clear()

    def flip(self):
        self.window.flip()
