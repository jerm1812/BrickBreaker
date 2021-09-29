from Brick import *


class Level:

    # Level
    level = 1

    # Brick proportions
    width, height = 0, 25

    # Brick array
    bricks = []

    def __init__(self, window, field):
        self.window, self.field, self.width = window, field, (field.x2 - field.x)/8

    def next_level(self):
        if self.level == 1:
            self.level_two()
        elif self.level == 2:
            self.level_three()

    def level_one(self):
        self.level = 1
        y = self.field.y
        for row in range(4):
            x = self.field.x
            for brick in range(8):
                hits = 1
                color = "mediumseagreen"
                if row == 0 or row == 2:
                    hits = 2
                    color = "darkseagreen"
                self.bricks.append(Brick(self.window, x, x + self.width, y, y + self.height, color, hits))
                x += self.width
            y += self.height

    def level_two(self):
        self.level = 2
        y = self.field.y
        for row in range(5):
            x = self.field.x - self.width
            for brick in range(8):
                x += self.width
                hits = 1
                color = "mediumseagreen"
                breakable = True
                spawn_ball = False
                if row == 1 or row == 3:
                    if brick == 1 or brick == 6:
                        continue
                    hits = 2
                    color = "darkseagreen"
                elif row == 2:
                    if brick != 3:
                        continue
                    x += self.width/2
                    spawn_ball = True
                    color = "orchid"
                self.bricks.append(Brick(self.window, x, x + self.width, y, y + self.height, color, hits, breakable, spawn_ball))
            y += self.height

    def level_three(self):
        self.level = 3
        y = self.field.y
        for row in range(8):
            x = self.field.x - self.width
            for brick in range(8):
                x += self.width
                hits = 1
                color = "mediumseagreen"
                breakable = True
                if row % 2 == 0:
                    hits = 2
                    color = "darkseagreen"
                    if brick < row / 2 or brick > 7 - row / 2:
                        continue
                if row % 2 == 1:
                    if brick == 0:
                        x -= self.width/2
                        continue
                    elif brick < row / 2 or brick > 8 - row / 2:
                        continue
                    elif row == 7:
                        color = "purple"
                        breakable = False

                self.bricks.append(Brick(self.window, x, x + self.width, y, y + self.height, color, hits, breakable))
            y += self.height
