from pyglet import canvas


class SystemStuff:
    @staticmethod
    def get_screen_resolution():
        display = canvas.Display()
        screen = display.get_default_screen()
        return screen.width, screen.height
