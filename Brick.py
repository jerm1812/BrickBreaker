from graphics import Rectangle, Point
import BrickType


class Brick:

    # Brick attributes
    hits = 0
    brick_type = 0

    def __init__(self, window, x, x2, y, y2, color, hits=1, breakable=True, spawn_ball=False):
        self.obj = Rectangle(Point(x, y), Point(x2, y2)).draw(window)
        self.obj.setFill(color)
        self.hits, self.breakable, self.spawn_ball = hits, breakable, spawn_ball
