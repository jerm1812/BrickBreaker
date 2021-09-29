from graphics import Rectangle, Point


class Paddle:

    # Velocity
    vel = 0

    # Constructor
    def __init__(self, window, x, x2, y, y2):
        self.obj = Rectangle(Point(x, y), Point(x2, y2)).draw(window)
        self.obj.setFill("lightblue")
