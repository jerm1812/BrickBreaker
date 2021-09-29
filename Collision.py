from graphics import Rectangle


class Collision:

    # Determines which kind of collision
    def determine_collision(self, ball, field, bricks, paddle):
        c = self.wall_collision(ball, field)
        if c is None:
            return
        elif c == "abyss":
            return ball
        elif not bricks:
            return
        elif bricks[-1].obj.getP2().getY() + 5 < ball.obj.getCenter().getY() < paddle.obj.getP1().getY() - 5:
            return
        elif paddle.obj.getP1().getY() - 5 < ball.obj.getCenter().getY():
            self.closest_point(ball, paddle, "p")
        else:
            for brick in bricks:
                b = self.closest_point(ball, brick)
                if b is not None:
                    return b

    # Bounces balls off of wall
    def wall_collision(self, ball, field):
        if (ball.obj.getCenter().getX() - ball.obj.getRadius() <= field.x
                or ball.obj.getCenter().getX() + ball.obj.getRadius() >= field.x2):
            ball.x_vel *= -1
            return
        elif ball.obj.getCenter().getY() - ball.obj.getRadius() <= field.y:
            ball.y_vel *= -1
            return
        elif ball.obj.getCenter().getY() + ball.obj.getRadius() >= field.y2:
            ball.y_vel *= -1
            return "abyss"
        else:
            return ""

    def closest_point(self, ball, rect, object_type="b",):
        bx, by, br = ball.obj.getCenter().getX(), ball.obj.getCenter().getY(), ball.obj.getRadius()
        rx, ry, rx2, ry2 = rect.obj.getP1().getX(), rect.obj.getP1().getY(), rect.obj.getP2().getX(), rect.obj.getP2().getY()
        delta_x = bx - max(rx, min(bx, rx + (rx2-rx)))
        delta_y = by - max(ry, min(by, ry + (ry2-ry)))
        if delta_x * delta_x + delta_y * delta_y < br * br:
            if object_type == "b":
                self.process_brick_bounce(ball, bx, by, rx, ry, rx2, ry2)
                return rect
            else:
                self.determine_paddle_hit(ball, bx, rx, rx2)

    def process_brick_bounce(self, ball, bx, by, rx, ry, rx2, ry2):
        if rx < bx < rx2:
            ball.y_vel *= -1
        elif ry < by < ry2:
            ball.x_vel *= -1
        else:
            ball.y_vel *= -1
            ball.x_vel *= -1

    def determine_paddle_hit(self, ball, bx, rx, rx2):
        if bx < rx + 40:
            hit = "l_edge"
        elif rx2 - 40 < bx:
            hit = "r_edge"
        elif rx + 40 < bx < rx + 80:
            hit = "l_middle"
        elif rx2 - 80 < bx < rx2 - 40:
            hit = "r_middle"
        elif rx + 80 < bx < rx2 - 80:
            ball.y_vel *= -1
            return
        else:
            ball.x_vel *= -1
            return

        self.process_paddle_bounce(ball, hit)

    def process_paddle_bounce(self, ball, hit):
        if ball.x_vel > 0:
            if hit == "r_edge":
                ball.x_vel *= 1.5
            elif hit == "l_edge":
                ball.x_vel *= -1
            elif hit == "r_middle":
                ball.x_vel *= 1.25
            elif hit == "l_middle":
                ball.x_vel *= .25
        else:
            if hit == "r_edge":
                ball.x_vel *= -1
            elif hit == "l_edge":
                ball.x_vel *= 1.5
            elif hit == "r_middle":
                ball.x_vel *= .25
            elif hit == "l_middle":
                ball.x_vel *= 1.25

        min_vel, max_vel = ball.min_vel, ball.max_vel
        ball.x_vel = min_vel if ball.x_vel < min_vel else max_vel if ball.x_vel > max_vel else ball.x_vel
        ball.x_vel = 1 if 0 < ball.x_vel < 1 else -1 if 0 > ball.x_vel > -1 else ball.x_vel
        ball.y_vel *= -1
