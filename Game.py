from graphics import *
from inputlistener import *
from Field import *
from Ball import *
from Paddle import *
from Scoreboard import *
from Collision import *
from Level import *
from Button import *


class Game:

    # Window proportions
    window_width, window_height = 1200, 700
    field_x, field_x2, field_y, field_y2 = 25, window_width - 25, 75, window_height - 25
    center = window_width / 2

    # Placeholders
    game_running = False
    balls = []
    buttons = []
    abyss_enabled = True

    def __init__(self):
        # Drawing window
        self.window = GraphWin("BrickBreaker", self.window_width, self.window_height)
        self.field = Field(self.window, self.field_x, self.field_x2, self.field_y, self.field_y2)
        self.scoreboard = Scoreboard(self.window, self.field_y)
        self.paddle = Paddle(self.window, self.center - 100, self.center + 100, self.field_y2 - 50, self.field_y2 - 25)
        self.create_buttons()

        # Setting up winning and losing text
        self.winning_text = Text(Point(self.center, 400), "").draw(self.window)
        self.losing_text = Text(Point(self.center, 400), "").draw(self.window)

        # Setting up abyss text
        self.abyss_off = Text(Point(self.center, 500), "").draw(self.window)

        # Setting up events
        self.events = InputListener(self.window)
        self.setup_event_handlers()

        # Classes
        self.collision = Collision()
        self.levels = Level(self.window, self.field)

        # Game setup
        self.setup_game()

    # Creates buttons
    def create_buttons(self):
        self.buttons.append(Button(self.window, self.window_width-150, self.window_width-30, 10, 60, "Disable Abyss"))
        self.buttons.append(Button(self.window, self.window_width-280, self.window_width-160, 10, 60, "Restart"))
        self.buttons.append(Button(self.window, self.window_width-410, self.window_width-290, 10, 60, "Start"))

    # Sets up the event handlers
    def setup_event_handlers(self):
        self.events.setKeyPressHandler(self.key_press)
        self.events.setKeyReleaseHandler(self.key_release)
        self.events.setMouseClickHandler(self.button_click)

    # Key and click events
    def key_press(self, key):
        if key == "Left" or key == "a":
            self.paddle.vel = -5
        elif key == "Right" or key == "d":
            self.paddle.vel = 5

    def key_release(self, key):
        if key == "Left" or key == "a" or key == "Right" or key == "d":
            self.paddle.vel = 0

    def button_click(self, point):
        for button in self.buttons:
            if button.obj.getP1().getX() < point.getX() < button.obj.getP2().getX() and button.obj.getP1().getY() < point.getY() < button.obj.getP2().getY():
                self.process_button(self.buttons.index(button))
                break
    # End key and click events

    # Process the button clicks
    def process_button(self, i):
        if i == 0:
            self.abyss_enabled = not self.abyss_enabled
            button_text = "Disable Abyss" if self.abyss_enabled else "Enable Abyss"
            abyss_text = "" if self.abyss_enabled else "Abyss disabled"
            self.buttons[0].text.setText(button_text)
            self.abyss_off.setText(abyss_text)
        elif i == 1:
            self.restart_game()
        elif i == 2:
            self.game_running = True

    # Restarts the game
    def restart_game(self):
        self.clear_balls()
        self.clear_bricks()
        self.reset_text()
        self.game_running = False
        self.center_paddle()
        self.setup_game()

    def reset_text(self):
        self.losing_text.setText("")
        self.winning_text.setText("")

    # Resets the scoreboard
    def reset_scoreboard(self):
        self.scoreboard.lives = 5
        self.scoreboard.score = 0
        self.update_lives()
        self.update_score()

    # Clears all balls
    def clear_balls(self):
        for ball in self.balls:
            ball.obj.undraw()
        self.balls.clear()

    # Clears all bricks
    def clear_bricks(self):
        for brick in self.levels.bricks:
            brick.obj.undraw()
        self.levels.bricks.clear()

    # Centers the paddle
    def center_paddle(self):
        self.paddle.obj.move(self.center - 100 - self.paddle.obj.getP1().getX(), 0)

    # Setts the game up
    def setup_game(self):
        self.levels.level_one()
        self.new_ball()
        self.waiting()
        self.game_loop()

    # Waits until start is pressed
    def waiting(self):
        while self.game_running is False:
            update(10)

    # Moves objects
    def move_objects(self):
        self.move_paddle()
        self.move_balls()
        self.check_collision()

    # Moves the paddle
    def move_paddle(self):
        # If paddle is inside field
        if (self.paddle.vel < 0 and self.paddle.obj.getP1().getX() > self.field_x
                or self.paddle.vel > 0 and self.paddle.obj.getP2().getX() < self.field_x2):
            if self.paddle.obj.getP1().getX() + self.paddle.vel < self.field_x:  # If vel is bigger than needed move
                self.paddle.obj.move(self.paddle.obj.getP1().getX() - self.field_x + self.paddle.vel, 0)
            elif self.paddle.obj.getP2().getX() + self.paddle.vel > self.field_x2:  # If vel is bigger than needed move
                self.paddle.obj.move(self.paddle.obj.getP2().getX() - self.field_x2 + self.paddle.vel, 0)
            else:  # Else normal paddle movement
                self.paddle.obj.move(self.paddle.vel, 0)

    # Moves all balls
    def move_balls(self):
        # Loops through balls
        for ball in self.balls:
            # If x_vel is bigger than needed move
            if ball.obj.getCenter().getX() - ball.obj.getRadius() + ball.x_vel < self.field_x and ball.x_vel < 0:
                ball.obj.move(ball.obj.getCenter().getX() - ball.obj.getRadius() + ball.x_vel - self.field_x, 0)
            elif ball.obj.getCenter().getX() + ball.obj.getRadius() + ball.x_vel > self.field_x2 and ball.x_vel > 0:
                ball.obj.move(ball.obj.getCenter().getX() + ball.obj.getRadius() + ball.x_vel - self.field_x2, 0)
            elif ball.obj.getCenter().getY() - ball.obj.getRadius() + ball.y_vel < self.field_y and ball.y_vel < 0:
                ball.obj.move(ball.obj.getCenter().getY() - ball.obj.getRadius() + ball.y_vel - self.field_y, 0)
            elif ball.obj.getCenter().getY() + ball.obj.getRadius() + ball.y_vel > self.field_y2 and ball.y_vel > 0:
                ball.obj.move(ball.obj.getCenter().getY() + ball.obj.getRadius() + ball.y_vel - self.field_y2, 0)
            else:
                ball.obj.move(ball.x_vel, ball.y_vel)

    # Checks the balls for collision
    def check_collision(self):
        for ball in self.balls:
            self.process_collision(self.collision.determine_collision(ball, self.field, self.levels.bricks, self.paddle))

    # Processes the collision
    def process_collision(self, collision):
        if type(collision) == Ball:
            self.hit_abyss(collision)
        elif collision is not None:
            self.hit_brick(collision)

    # Hits a brick
    def hit_brick(self, brick):
        if brick is not None:
            brick.hits -= 1
            if brick.hits <= 0 and brick.breakable:
                brick.obj.undraw()
                self.levels.bricks.remove(brick)
                self.scoreboard.score += 1
                self.scoreboard.update_score()
                if brick.spawn_ball:
                    self.new_ball()

    # Moves to next level
    def next_level(self):
        self.clear_balls()
        if self.levels.level < 3:
            self.levels.next_level()
            self.scoreboard.update_level()
            self.new_ball()
        else:
            self.win_game()

    # Sets game to win
    def win_game(self):
        self.display_win()
        self.pause_game()

    # Pauses game
    def pause_game(self):
        self.game_running = False
        self.waiting()

    # Displays win
    def display_win(self):
        self.winning_text.setText("Congratulations you won!")

    def display_loss(self):
        self.losing_text.setText("Game over!")

    # Creates a new ball
    def new_ball(self):
        self.balls.append(Ball(self.window, self.paddle.obj.getP1().getX()+100, self.paddle.obj.getP1().getY()-50, 10))

    # Processes ball going into the abyss
    def hit_abyss(self, ball):
        if self.abyss_enabled:
            self.remove_ball(ball)
            if len(self.balls) == 0:
                self.scoreboard.lives -= 1
                self.scoreboard.update_lives()
                self.new_ball()

    # Removes a ball
    def remove_ball(self, ball):
        ball.obj.undraw()
        self.balls.remove(ball)

    def bricks_remaining(self):
        if len(self.levels.bricks) == 1 and not self.levels.bricks[0].breakable:
            return False
        return self.levels.bricks

    # Main game loop
    def game_loop(self):
        while True:
            while self.bricks_remaining() and self.balls and self.scoreboard.lives:
                self.move_objects()
                update(150)
            if not self.scoreboard.lives:
                break
            self.next_level()
        self.display_loss()
        self.pause_game()
