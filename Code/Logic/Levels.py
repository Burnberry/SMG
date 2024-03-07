import math

from Code.Logic.LevelScene import LevelScene
from Code.Util.Assets import Img
from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Logic.Box import Digit


class Level0(LevelScene):
    def __init__(self, game):
        super().__init__(game, "L0")
        self.minMoves = 1
        text = ["Find Tommy the mundane"]
        self.levelText = self.make_level_text_box(text)
        text = ["Click on a square", "to look into a box"]
        self.levelMechanicsText = self.make_level_text_box(text, "bl")

    def restart_level(self):
        x, y = self.game.camera.get_center()
        self.boxStates[0] = True
        self.make_box((x, y), 0)

    def move_cat(self):
        pass


class Level1(LevelScene):
    def __init__(self, game):
        super().__init__(game, "L1")
        self.minMoves = 3
        text = ["Find Furball the three-legged", "", "after each move: stays or teleports right"]
        self.levelText = self.make_level_text_box(text)
        text = ["All cats know which boxes you'll open beforehand", "they try to stay hidden for as long as possible"]
        self.levelMechanicsText = self.make_level_text_box(text, "bl")

    def restart_level(self):
        x, y = self.game.camera.get_center()
        for key in range(3):
            self.boxStates[key] = True
            self.make_box((x + 20 * (key - 1), y), key)

    def move_cat(self):
        states_new = {i: False for i in range(3)}
        states_new[2] = self.boxStates[2]
        for key in range(2):
            if self.boxStates[key]:
                states_new[key] = True
                states_new[key+1] = True

        self.boxStates = states_new


class Level2(LevelScene):
    def __init__(self, game):
        super().__init__(game, "L2")
        self.minMoves = 5
        text = ["Find Scratchy the drunk", "", "after each move, teleports clock wise"]
        self.levelText = self.make_level_text_box(text)
        text = ["Helper mode can give useful information", "It crosses out boxes where a cat can't be"]
        self.levelMechanicsText = self.make_level_text_box(text, "bl")

    def restart_level(self):
        x0, y0 = self.game.camera.get_center()
        r, pi = 25, math.pi
        for i in range(5):
            self.boxStates[i] = True
            x = x0 + r*math.sin(2*pi*i/5)
            y = y0 + r*math.cos(2*pi*i/5)
            self.make_box((x, y), i)

    def move_cat(self):
        states_new = {i: False for i in range(5)}
        for key in range(5):
            if self.boxStates[key]:
                new_key = (key+1) % 5
                states_new[new_key] = True

        self.boxStates = states_new


class Level3(LevelScene):
    def __init__(self, game):
        super().__init__(game, "L3")
        self.minMoves = 6
        text = ["Find Snowball the elusive", "", "After each move, teleports left or right"]
        self.levelText = self.make_level_text_box(text)

    def restart_level(self):
        x, y = self.game.camera.get_center()
        for key in range(5):
            self.boxStates[key] = True
            self.make_box((x + 20 * (key - 2), y), key)

    def move_cat(self):
        states_new = {i: False for i in range(5)}
        for key in range(5):
            if self.boxStates[key]:
                if key + 1 < 5:
                    states_new[key+1] = True
                if key - 1 >= 0:
                    states_new[key-1] = True

        self.boxStates = states_new


class LevelA0(LevelScene):
    def __init__(self, game):
        self.noBarrier = True
        super().__init__(game, "A0")
        self.minMoves = 2
        text = ["Find Tom the unlucky", "", "After each move cat can:", "-stay", "-teleport left and right"]
        self.levelText = self.make_level_text_box(text)
        text = ["New: Anti-magic barriers", "cats can't teleport through them", "Moved with buttons, at most once per turn", "Remember: A cat moves after you look into a box"]
        self.levelMechanicsText = self.make_level_text_box(text, "bl")

        x, y = self.game.camera.get_center()
        renderer = self.game.renderer
        dx, dy = 22, 25
        self.leftButton = renderer.make_ui_visual(x-dx, y+dy, Img.ArrowLeft, renderer.UI, "cc")
        self.rightButton = renderer.make_ui_visual(x+dx, y+dy, Img.ArrowRight, renderer.UI, "cc")

    def restart_level(self):
        self.barrierPosition = 0
        self.barrierMovable = True
        x, y = self.game.camera.get_center()
        for key in range(2):
            self.boxStates[key] = True
            self.make_box((x - 11 + 22 * key, y), key)

        if self.noBarrier:
            self.noBarrier = False
            self.barrier = self.make_barrier((x-3-8-11, y))
        self.barrier.set_position(x-3-8-11, y)

    def handle_input(self, dt):
        super().handle_input(dt)
        movable = self.barrierMovable
        controller = self.game.controller
        for button in [self.rightButton, self.leftButton]:
            if button.inside(*controller.mouse_position) and movable:
                button.set_color((255, 255, 127))
            else:
                button.set_color((255, 255, 255))
        if not movable:
            return

        if self.rightButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
            self.move_barrier(right=True)
        if self.leftButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
            self.move_barrier(right=False)

    def move_barrier(self, right=True):
        self.barrierMovable = False
        if right:
            dx = 22
            self.barrierPosition += 1
        else:
            dx = -22
            self.barrierPosition -= 1
        x, y = self.barrier.get_position()
        self.barrier.set_position(x+dx, y)

    def move_cat(self):
        self.barrierMovable = True
        states_new = {i: False for i in range(3)}
        for key in range(2):
            if self.boxStates[key]:
                states_new[key] = True
                if key + 1 < 2 and self.barrierPosition != key+1:
                    states_new[key + 1] = True
                if key - 1 >= 0 and self.barrierPosition != key:
                    states_new[key - 1] = True

        self.boxStates = states_new


class LevelA1(LevelScene):
    def __init__(self, game):
        self.noBarrier = True
        super().__init__(game, "A1")
        self.minMoves = 3
        text = ["Find Felix the pyromancer", "", "After each move cat can:", "-stay", "-teleport left and right"]
        self.levelText = self.make_level_text_box(text)

        renderer = self.game.renderer
        x, y = self.game.camera.get_center()
        dx, dy = 22, 25
        self.leftButton = renderer.make_ui_visual(x-dx, y+dy, Img.ArrowLeft, renderer.UI, "cc")
        self.rightButton = renderer.make_ui_visual(x+dx, y+dy, Img.ArrowRight, renderer.UI, "cc")

    def restart_level(self):
        self.barrierPosition = 0
        self.barrierMovable = True
        x, y = self.game.camera.get_center()
        for key in range(3):
            self.boxStates[key] = True
            self.make_box((x + 22 * (key - 1), y), key)
        if self.noBarrier:
            self.noBarrier = False
            self.barrier = self.make_barrier((x-3-8-22*1, y))
        self.barrier.set_position(x-3-8-22*1, y)

    def handle_input(self, dt):
        super().handle_input(dt)
        movable = self.barrierMovable
        controller = self.game.controller
        for button in [self.rightButton, self.leftButton]:
            if button.inside(*controller.mouse_position) and movable:
                button.set_color((255, 255, 127))
            else:
                button.set_color((255, 255, 255))
        if not movable:
            return

        if self.rightButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
            self.move_barrier(right=True)
        if self.leftButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
            self.move_barrier(right=False)

    def move_barrier(self, right=True):
        self.barrierMovable = False
        if right:
            dx = 22
            self.barrierPosition += 1
        else:
            dx = -22
            self.barrierPosition -= 1
        x, y = self.barrier.get_position()
        self.barrier.set_position(x+dx, y)

    def move_cat(self):
        self.barrierMovable = True
        states_new = {i: False for i in range(3)}
        for key in range(3):
            if self.boxStates[key]:
                states_new[key] = True
                if key + 1 < 3 and self.barrierPosition != key+1:
                    states_new[key + 1] = True
                if key - 1 >= 0 and self.barrierPosition != key:
                    states_new[key - 1] = True

        self.boxStates = states_new


class LevelB(LevelScene):
    def __init__(self, game):
        self.buttonExists = False
        super().__init__(game, "L4")
        self.minMoves = 2
        text = ["Find Smudge the grumpy", "", "After each move cat can:", "-stay", "-teleport left or right"]
        self.levelText = self.make_level_text_box(text)
        text = ["New mechanic: Boost button", "Each move you can press the button once",
                "This lets you look into an extra box", "in a single move without the cat", "teleporting",
                "The button has a limited number of uses"]

        self.mechanicText = self.make_level_text_box(text, "bl")

        renderer = self.game.renderer
        x, y = self.game.camera.get_screen_center()
        dy = 25*SettingsGlobal.Scale
        self.boostButton = renderer.make_ui_text_box(x, y + dy, "Boost " + str(self.boosters) + "X", renderer.UI, renderer.Text, "cc")
        self.buttonExists = True

    def restart_level(self):
        self.boosters = 2
        self.boostable = True
        self.boosted = False

        if self.buttonExists:
            self.boostButton.set_text("Boost " + str(self.boosters) + "X")
            self.boostButton.set_color((255, 255, 255))
        x, y = self.game.camera.get_center()
        for key in range(3):
            self.boxStates[key] = True
            self.make_box((x + 20 * (key - 1), y), key)
        for key in range(3):
            self.boxStates[key] = True

    def move_cat(self):
        self.barrierMovable = True
        states_new = {i: False for i in range(3)}
        for key in range(3):
            if self.boxStates[key]:
                states_new[key] = True
                if key + 1 < 3:
                    states_new[key + 1] = True
                if key - 1 >= 0:
                    states_new[key - 1] = True

        self.boxStates = states_new

    def openBox(self, key):
        if self.boosted:
            self.boosted = False
            self.boostButton.set_color((255, 127, 127))
            self.move(key)
            if self.check_win():
                self.win()
            return
        if self.boosters > 0:
            self.boostable = True
            self.boostButton.set_color((255, 255, 255))
        super().openBox(key)

    def boost(self):
        self.boosters -= 1
        self.boosted = True
        self.boostable = False
        self.boostButton.set_text("Boost " + str(self.boosters) + "X")
        self.boostButton.set_color((127, 255, 127))

    def handle_input(self, dt):
        super().handle_input(dt)
        boostable = self.boosters > 0 and self.boostable
        controller = self.game.controller
        for button in [self.boostButton]:
            button.highlight(button.inside(*controller.mouse_position) and boostable)
        if not boostable:
            return

        if self.boostButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
            self.boostButton.set_color((127, 255, 127))
            self.boost()


class LevelF(LevelScene):
    def __init__(self, game):
        self.buttonExists = False
        self.helpCountDict = {}
        super().__init__(game, "L5")
        self.minMoves = 6
        text = ["Find chonkers", "", "After each move cat can:", "-stay", "-teleport left or right", "",
                "Cat needs to eat frequently and can:", "-move or stay up to 4 times without eating"]
        self.levelText = self.make_level_text_box(text)
        text = ["Cats are dramatic and always act as if", "they're about to starve", "They will go to their food bowls "
                "often", "and make sure they can always reach a bowl", "without 'starving'"]
        self.mechanicText = self.make_level_text_box(text, "bl")

        renderer = self.game.renderer
        x, y = self.game.camera.get_screen_center()
        dy = 25*SettingsGlobal.Scale
        self.boostButton = renderer.make_ui_text_box(x, y + dy, "Boost " + str(self.boosters) + "X", renderer.UI, renderer.Text, "cc")
        self.buttonExists = True

    def restart(self):
        for key in self.helpCountDict:
            self.helpCountDict[key].remove()
        self.helpCountDict = {}
        super().restart()

    def restart_level(self):
        self.boosters = 2
        self.boostable = True
        self.boosted = False

        if self.buttonExists:
            self.boostButton.set_text("Boost " + str(self.boosters) + "X")
            self.boostButton.set_color((255, 255, 255))
        x, y = self.game.camera.get_center()
        for key in self.helpCountDict:
            self.helpCountDict[key].remove()
        for key in range(5):
            self.boxStates[key] = True
            self.make_box((x + 20 * (key - 2), y), key)
            if key == 0 or key == 4:
                box = self.boxesDict[key]
                box.set_assets(Img.FoodBowl, Img.FoodBowlCrossed)
            digit = Digit((x + 20 * (key - 2), y), "0")
            self.helpCountDict[key] = digit
            renderer = self.game.renderer
            renderer.make_visual_image(digit, renderer.Text, "cc")
            digit.set_visibility(False)

        for key in range(5):
            val = max(key, 4-key)
            self.boxStates[key] = val

    def move_cat(self):
        states_new = {i: self.boxStates[i] - 1 for i in range(5)}
        for key in range(5):
            if self.boxStates[key] > 0:
                if key + 1 < 5 and self.boxStates[key] + key >= 4:
                    val = max(self.boxStates[key] - 1, states_new[key+1])
                    states_new[key+1] = val

                if key - 1 >= 0 and self.boxStates[key] - key >= 0:
                    val = max(self.boxStates[key] - 1, states_new[key - 1])
                    states_new[key - 1] = val
        if states_new[0] >= 0:
            states_new[0] = 4
        if states_new[4] >= 0:
            states_new[4] = 4

        for key in states_new:
            if max(states_new[key]-key, states_new[key] - (4-key)) < 0:
                states_new[key] = False

        self.boxStates = states_new

    def openBox(self, key):
        if self.boosted:
            self.boosted = False
            self.boostButton.set_color((255, 127, 127))
            self.move(key)
            if self.check_win():
                self.win()
            return
        if self.boosters > 0:
            self.boostable = True
            self.boostButton.set_color((255, 255, 255))
        super().openBox(key)

    def boost(self):
        self.boosters -= 1
        self.boosted = True
        self.boostable = False
        self.boostButton.set_text("Boost " + str(self.boosters) + "X")
        self.boostButton.set_color((127, 255, 127))

    def handle_input(self, dt):
        super().handle_input(dt)
        boostable = self.boosters > 0 and self.boostable
        controller = self.game.controller
        for button in [self.boostButton]:
            button.highlight(button.inside(*controller.mouse_position) and boostable)
        if not boostable:
            return

        if self.boostButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
            self.boostButton.set_color((127, 255, 127))
            self.boost()

    def update_helper(self):
        super().update_helper()
        for key in self.boxesDict:
            if self.helper and self.boxStates[key] > 0:
                self.helpCountDict[key].set_digit(str(self.boxStates[key]))
                self.helpCountDict[key].set_visibility(True)
            else:
                self.helpCountDict[key].set_visibility(False)
