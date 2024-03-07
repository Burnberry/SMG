class Camera:
    def __init__(self, x, y, screen_width, screen_height, offset):
        self.screenWidth, self.screenHeight = screen_width, screen_height
        self.offset = offset
        self.x, self.y = x, y
        self.w, self.h = screen_width//offset, screen_height//offset

    def inside(self, x, y):
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    def to_game_coords(self, cx, cy):
        return self.x + cx/self.offset, self.y + cy/self.offset

    def to_screen_coords(self, x, y):
        return (x - self.x)*self.offset, (y - self.y)*self.offset

    def set_location(self, x, y):
        self.x, self.y = x, y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_center(self):
        x, y = self.x + self.w/2, self.y + self.h/2
        return x, y

    def get_screen_center(self):
        return self.screenWidth//2, self.screenHeight//2

    def get_screen_position(self, anchor):
        w, h = self.screenWidth, self.screenHeight
        cx, cy = 0, 0
        ax, ay = anchor[1], anchor[0]
        if ax == 'c':
            cx = w // 2
        elif ax == 'r':
            cx = w - 1

        if ay == 'c':
            cy = h // 2
        elif ay == 't':
            cy = h - 1

        return cx, cy
