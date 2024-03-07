from Code.Util.Assets import Img, Alpha

from Code.Util.Scene import Scene
from Code.Util.Renderer import Renderer
from Code.Logic.SaveState import SaveState
from Code.Util.SettingsGlobal import SettingsGlobal


class MainScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        anchor = "bc"
        x, y = self.game.camera.get_screen_position(anchor)
        renderer = self.game.renderer
        y += 20*SettingsGlobal.Scale

        self.pygletText = renderer.make_ui_text_box(x, y, "Made using pyglet", renderer.UI, renderer.Text, anchor)
        w, h = self.pygletText.get_onscreen_dimensions()
        y += h
        self.logo = renderer.make_ui_visual(x, y, Img.PygletLogo, renderer.UI, anchor)

        self.create_level_selector()

    def update(self, dt):
        self.handle_input(dt)

    def handle_input(self, dt):
        controller = self.game.controller
        for level in self.levelButtonDict:
            button = self.levelButtonDict[level]
            button.highlight(button.inside(*controller.mouse_position))
            if button.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
                self.switchState = level
                break

    def create_level_selector(self):
        self.levelButtonDict = {}
        x, y = self.game.camera.get_screen_center()
        x -= (8 + 2*16)*SettingsGlobal.Scale
        for level in SaveState.leveStates:
            minMoves, rMoves = SaveState.leveStates[level]
            button = self.game.renderer.make_ui_text_box(x, y, level, Renderer.UI, Renderer.Text, 'cc')
            x += 16 * SettingsGlobal.Scale
            if minMoves == -1:
                button.set_color((90, 90, 90))
                continue
            if minMoves == rMoves:
                button.set_color((127, 255, 127))
            self.levelButtonDict[level] = button
