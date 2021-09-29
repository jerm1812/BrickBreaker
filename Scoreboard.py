from graphics import Text, Point


class Scoreboard:

    # Score
    score = 0
    lives = 5
    level = 1

    # Constructor
    def __init__(self, window, field_y, level=1):
        x1, x2, x3, x4, x5, x6, y = 100, 150, 250, 300, 400, 450, field_y / 2

        Text(Point(x1, y), "Score:").draw(window)
        self.score_txt = Text(Point(x2, y), str(self.score)).draw(window)
        Text(Point(x3, y), "Lives:").draw(window)
        self.lives_txt = Text(Point(x4, y), str(self.lives)).draw(window)
        Text(Point(x5, y), "Level:").draw(window)
        self.level_txt = Text(Point(x6, y), str(level)).draw(window)

    def update_lives(self):
        self.lives_txt.setText(str(self.lives))

    # Updates the score on scoreboard
    def update_score(self):
        self.score_txt.setText(str(self.score))

    # Updates the level on scoreboard
    def update_level(self):
        self.level_txt.setText(str(self.level))
