from abc import abstractmethod

from Code.Util.SettingsGlobal import SettingsGlobal
from Code.Util.Assets import Img
from Code.Util.Scene import Scene
from Code.Util.Renderer import Renderer
from Code.Logic.Box import Box
from Code.Logic.Barrier import Barrier
from Code.Logic.SaveState import SaveState


class LevelScene(Scene):
    def __init__(self, game, name):
        super().__init__(game)

        self.name = name
        self.boxesDict = {}
        self.boxStates = {}
        self.moves = 0
        self.minMoves = 0
        self.won = False
        self.helper = False

        anchor = "tr"
        renderer = self.game.renderer
        x, y = self.game.camera.get_screen_position(anchor)
        self.backButton = renderer.make_ui_text_box(x, y, "BACK", Renderer.UI, Renderer.Text, anchor)
        x -= self.backButton.get_onscreen_dimensions()[0]
        self.restartButton = renderer.make_ui_text_box(x, y, "RESTART", Renderer.UI, Renderer.Text, anchor)
        x -= self.restartButton.get_onscreen_dimensions()[0]
        self.helperButton = renderer.make_ui_text_box(x, y, "HELP MODE", Renderer.UI, Renderer.Text, anchor)
        x -= self.helperButton.get_onscreen_dimensions()[0]
        self.moveCounter = renderer.make_ui_text_box(x, y, str(self.moves) + " MOVES", Renderer.UI, Renderer.Text, anchor)
        self.continueButton = renderer.make_ui_text_box(-1, -1, "Continue", Renderer.UI, Renderer.Text, anchor)
        self.movesMessage = renderer.make_ui_text_box(-1, -1, "Level can be done with fewer moves", Renderer.UI, Renderer.Text, anchor)

        self.restart()

    def restart(self):
        print()
        self.moves = 0
        self.won = False
        self.continueButton.set_anchor("tr")
        self.continueButton.set_position(-1, -1)
        self.movesMessage.set_anchor("tr")
        self.movesMessage.set_position(-1, -1)
        self.updateMoveCounter()
        self.moveCounter.set_text(str(self.moves) + " MOVES")

        for key in self.boxesDict:
            self.boxesDict[key].remove()
        self.boxesDict = {}
        self.boxStates = {}

        self.restart_level()

    @abstractmethod
    def restart_level(self):
        pass

    @abstractmethod
    def move_cat(self):
        pass

    def make_box(self, position, key):
        box = Box(position)
        self.game.renderer.make_visual_image(box, self.game.renderer.Foreground, "cc")
        self.boxesDict[key] = box

    def make_barrier(self, position):
        barrier = Barrier(position)
        self.game.renderer.make_visual_image(barrier, self.game.renderer.Foreground, "cc")
        return barrier

    def updateMoveCounter(self):
        self.moveCounter.set_text(str(self.moves) + " MOVES")

    def update(self, dt):
        self.handle_input(dt)
        self.update_helper()

    def handle_input(self, dt):
        controller = self.game.controller
        for button in [self.backButton, self.restartButton, self.helperButton]:
            button.highlight(button.inside(*controller.mouse_position))

        if self.backButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
            self.switchState = "BACK"
        if self.restartButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
            self.restart()
        if self.helperButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
            if self.helper:
                self.helper = False
                self.helperButton.set_color((255, 255, 255))
            else:
                self.helper = True
                self.helperButton.set_color((127, 255, 127))
        if self.won:
            self.continueButton.highlight(self.continueButton.inside(*controller.mouse_position))
            if self.continueButton.inside(*controller.mouse_position) and controller.is_control_pressed(controller.click):
                self.switchState = "CONTINUE"

        mouse_position = controller.mouse_position
        for key in self.boxesDict:
            box = self.boxesDict[key]
            if self.won:
                on = False
            else:
                on = box.visual.inside(*mouse_position)
            box.highlight(on)

            if on and controller.is_control_pressed(controller.click):
                self.lastOpenedBox = key
                self.openBox(key)

    def openBox(self, key):
        x = ""
        for k in self.boxStates:
            if k == key:
                x += '🔎'
            elif self.boxStates[k]:
                x += '❔'
            else:
                x += '❌'
        x += " -> "
        self.moves += 1
        self.updateMoveCounter()
        self.move(key)
        if self.check_win():
            self.win()
        else:
            self.move_cat()
            for k in self.boxStates:
                if self.boxStates[k]:
                    x += '❔'
                else:
                    x += '❌'
            print(x)

    def move(self, key):
        self.boxStates[key] = False

    def check_win(self):
        for key in self.boxStates:
            if self.boxStates[key]:
                return False
        return True

    def win(self):
        self.won = True
        self.update_savestate()
        self.continueButton.set_anchor("cc")
        x, y = self.game.camera.get_screen_position("cc")
        y += 45*SettingsGlobal.Scale
        self.continueButton.set_position(x, y)
        if self.moves > self.minMoves:
            self.movesMessage.set_anchor("cc")
            y -= 8*SettingsGlobal.Scale
            self.movesMessage.set_position(x, y)
        self.boxesDict[self.lastOpenedBox].set_assets(Img.CatWizard, Img.CatWizard)

    def update_savestate(self):
        moves, n = SaveState.leveStates[self.name]
        if moves == 0:
            moves = self.moves
        moves = min(moves, self.moves)
        SaveState.leveStates[self.name] = (moves, n)

        level = "L" + str(int(self.name[1])+1)
        if level in SaveState.leveStates:
            moves, moves_needed = SaveState.leveStates[level]
            if moves == -1:
                SaveState.leveStates[level] = (0, moves_needed)

    def update_helper(self):
        for key in self.boxesDict:
            box = self.boxesDict[key]
            if self.helper:
                if self.boxStates[key]:
                    box.open()
                else:
                    box.cross()
            else:
                box.open()

    def make_level_text_box(self, text, anchor="tl"):
        renderer = self.game.renderer
        x, y = self.game.camera.get_screen_position(anchor)
        return renderer.make_ui_text_box(x, y, text, renderer.UI, renderer.Text, anchor)
