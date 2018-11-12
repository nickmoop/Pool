import time

from math_helper import vector_length


class Stick:
    def __init__(self):
        self.head = [0, 0]
        self.tail = [0, 0]
        self.length = 200
        self.item = None
        self.direction = [0, 0]
        self.color = 'firebrick'
        self.loss = 0.13

    def stick_hit_ball(self, board, balls, step_coefficient):
        dir_x = (self.head[0] - self.tail[0]) / self.length
        dir_y = (self.head[1] - self.tail[1]) / self.length
        self.direction = [dir_x, dir_y]
        timer = 0
        while timer < step_coefficient:
            time.sleep(1 / step_coefficient)
            x_front_new = self.head[0] + dir_x
            x_finish_new = self.tail[0] + dir_x
            y_start_new = self.head[1] + dir_y
            y_finish_new = self.tail[1] + dir_y
            self.head = [x_front_new, y_start_new]
            self.tail = [x_finish_new, y_finish_new]
            self.paint(board.item)
            for ball in balls:
                delta_x = ball.x - x_front_new
                delta_y = ball.y - y_start_new
                distance = vector_length(delta_x, delta_y)
                if distance < ball.radius:
                    return ball

            timer += 1

        return None

    def hit_ball_by_stick(self, ball, force, ball_field):
        r = 100
        x = ball_field.coordinates[0]
        y = ball_field.coordinates[1]
        ball_field.find_top_point_direction()  # RELATIVE!!!
        a = vector_length(x - 100, y - 100)
        v0 = force
        dM = float(1 / 3)
        h = a

        if a > 60:
            return False

        v1Numerator = v0 * (1 + dM) * (1 + (1 - self.loss - self.loss * (1 / dM) * (1 + 5 / 2 * ((a / r) ** 2))) ** 0.5)
        v1Denomenator = (1 + dM + 5 / 2 * ((a / r) ** 2)) * (1 + ((1 - self.loss - self.loss * (1 / dM)) ** 0.5))
        v1 = v1Numerator / v1Denomenator
        rR = (v1 * h * 5) / (2 * r)
        ball.pulse = v1
        ball.pulseSpin = rR
        ball.dx, ball.dy = self.direction
        dir_x = self.direction[0]
        dir_y = self.direction[1]
        x = -(ball_field.top_point[0] * dir_y - ball_field.top_point[1] * dir_x)
        y = ball_field.top_point[0] * dir_x + ball_field.top_point[1] * dir_y
        ball.spin = [x, y]

        return True

    def calculate_back_coordinates(self, x, y):
        dx = x - self.head[0]
        dy = y - self.head[1]
        length = ((dx ** 2) + (dy ** 2)) ** 0.5
        if length != 0 and length != self.length:
            coefficient_of_length = self.length / length
            x = coefficient_of_length * dx + self.head[0]
            y = coefficient_of_length * dy + self.head[1]

        self.tail = [x, y]

    def paint(self, field):
        if self.item:
            self.erase(field)

        self.item = field.create_line(
            self.head[0], self.head[1],
            self.tail[0], self.tail[1],
            fill=self.color
        )

    def erase(self, field):
        field.delete(self.item)