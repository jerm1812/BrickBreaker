from graphics import Rectangle, Point, Text


class Button:

    # Button state
    activated = False

    def __init__(self, window, x, x2, y, y2, text):
        self.obj = Rectangle(Point(x, y), Point(x2, y2)).draw(window)
        self.text = Text(Point(x+(x2-x)/2, y+(y2-y)/2), text).draw(window)

    def toggle_button(self):
        self.activated = not self.activated
