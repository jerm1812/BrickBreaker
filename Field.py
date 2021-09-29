from graphics import Rectangle, Point


class Field:

    # Position placeholders
    x, x2, y, y2 = 0, 0, 0, 0

    # Constructor
    def __init__(self, window, x, x2, y, y2):
        self.x, self.x2, self.y, self.y2 = x, x2, y, y2
        Rectangle(Point(x, y), Point(x2, y2)).draw(window)
