from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, game):
        self.game = game
        self.switchState = None

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def handle_input(self, dt):
        pass
