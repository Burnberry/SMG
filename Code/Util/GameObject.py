from abc import ABC, abstractmethod


class GameObject(ABC):
    active_objects = set()

    @staticmethod
    def update_active_objects(dt):
        for obj in GameObject.active_objects.copy():
            if obj in GameObject.active_objects:
                obj.update(dt)

    def __init__(self):
        self.associated_objects = set()

        GameObject.active_objects.add(self)

    @abstractmethod
    def update(self, dt):
        pass

    def remove(self):
        self.active_objects.remove(self)

        for obj in self.associated_objects:
            obj.signal_associate_removal(self)

    def add_associate(self, obj):
        self.associated_objects.add(obj)

    def remove_associate(self, obj):
        if obj in self.associated_objects:
            self.associated_objects.remove(obj)


class GameVisualObject(GameObject):
    def __init__(self, position, asset):
        super().__init__()

        self.x, self.y = position
        self.asset = asset
        self.visual = None

    @abstractmethod
    def update(self, dt):
        pass

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x, self.y = x, y

    def set_visual(self, visual):
        self.visual = visual
