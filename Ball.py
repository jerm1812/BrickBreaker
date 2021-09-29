from graphics import Circle, Point
from random import randrange


class Ball:

    # Velocities
    x_vel = 0
    y_vel = -1
    max_vel = 5
    min_vel = -5

    # Constructor
    def __init__(self, window, x, y, r):
        # Ball object
        self.obj = Circle(Point(x, y), r).draw(window)
        self.obj.setFill("red")
        # x velocity
        self.x_vel = randrange(-3, 3)
        self.x_vel = 1 if self.x_vel == 0 else self.x_vel
