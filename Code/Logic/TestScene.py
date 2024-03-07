from Code.Util.Assets import Img, Alpha

from Code.Util.Scene import Scene
from Code.Util.Renderer import Renderer
from Code.Logic.TestMovingBox import TestMovingBox


class TestScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        n = 1
        for i in range(n):
            test_obj = TestMovingBox(game.camera.get_center())
            test_obj.time_passed = i*2*3.14/n
            test_visual = self.game.renderer.make_visual_image(test_obj, Img.BoxClosed, Renderer.Foreground)

        x, y = 0, 0
        self.w, self.h = 16, 16
        self.test_UI = self.game.renderer.make_ui_box(x, y, self.w, self.h)
        self.test_UI_text = self.game.renderer.make_ui_text_box(x, y+100, "appel peer kalkoen??? .... flapper      he", Renderer.UI, Renderer.Text)

    def update(self, dt):
        self.w += 1
        self.test_UI.resize_element(self.w, self.h)

        self.test_UI_text.set_position(self.w, self.h + 100)

    def handle_input(self, dt):
        pass
