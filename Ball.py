from math_helper import vector_length, calculate_ball_direction, \
    calculate_ball_sign


class BallField:
    def __init__(self, canvas=None, board_wide=0):
        self.item = None
        self.point_of_hit = None
        self.rotation_axle = None
        self.canvas = canvas
        self.top_point = [0, 0, 0]
        self.board_wide = board_wide + 150
        self.coordinates = [0, 0]

    def paint(self, root_field):
        if self.canvas is None:
            return

        self.item = self.canvas(root_field)
        self.item.place(x=self.board_wide, y=85, width=200, height=200)
        self.item.create_oval(10, 10, 190, 190, fill='white', outline='black')
        self.item.create_line(10, 100, 190, 100, fill='black')
        self.item.create_line(100, 10, 100, 190, fill='black')
        self.point_of_hit = self.item.create_oval(
            0, 0, 0, 0, fill='red', outline='red')
        self.rotation_axle = self.item.create_line(0, 0, 0, 0, fill='red')

    def find_top_point_direction(self):
        dx = self.coordinates[0] - 100
        dy = self.coordinates[1] - 100
        length = vector_length(dx, dy)
        if length != 0:
            x_new = dx / length
            y_new = -dy / length
        else:
            x_new = 0
            y_new = 0

        self.top_point[0] = x_new
        self.top_point[1] = y_new


class Ball:
    def __init__(self, x=0, y=0, color='white'):
        self.color = color
        self.x = x
        self.y = y
        self.x_guess = 0
        self.y_guess = 0
        self.dx = 0
        self.dy = 0
        self.spin = [0, 0]
        self.item = None
        self.pulse = 0
        self.pulseSpin = 0
        self.radius = 5
        self.cloth_friction = 0.14
        self.board_friction = 0.20
        self.ball_friction = 0.03

        self.spin_item = None
        self.direction_item = None
        self.route_item = None

    def hit_ball_by_ball(self, ball_to_check):
        dx = self.x - ball_to_check.x
        dy = self.y - ball_to_check.y
        d = vector_length(dx, dy)
        sin_a = dx / d
        cos_a = dy / d

        if ball_to_check.pulse != 0:
            dir_new_x = cos_a * ball_to_check.dx + sin_a * ball_to_check.dy
            dir_new_y = -((-sin_a) * ball_to_check.dy + cos_a * ball_to_check.dx)
            ball_to_check.dx = dir_new_x * cos_a - dir_new_y * sin_a
            ball_to_check.dy = dir_new_x * sin_a + dir_new_y * cos_a

            dir_new_x = cos_a * self.dx + sin_a * self.dy
            dir_new_y = -((-sin_a) * self.dy + cos_a * self.dx)
            self.dx = dir_new_x * cos_a - dir_new_y * sin_a
            self.dy = dir_new_x * sin_a + dir_new_y * cos_a

            self.pulse, ball_to_check.pulse = ball_to_check.pulse, self.pulse
        else:
            dir_summ_x = self.dx
            dir_summ_y = self.dy
            ball_to_check.dx, ball_to_check.dy = -sin_a, -cos_a
            dir_ball = calculate_ball_direction(-sin_a, -cos_a)
            sign_ball = calculate_ball_sign(self.dx, self.dy, -sin_a, -cos_a)
            self.dx = dir_ball[0] * sign_ball[0]
            self.dy = dir_ball[1] * sign_ball[1]
            self.update_pulse(dir_summ_x, dir_summ_y, self.pulse)
            ball_to_check.update_pulse(dir_summ_x, dir_summ_y, self.pulse)

    def hit_ball_by_ballx2(self, ball_to_check_1, ball_to_check_2):
        dx = self.x - ball_to_check_1.x
        dy = self.y - ball_to_check_1.y
        d = vector_length(dx, dy)
        sin_a = dx / d
        cos_a = dy / d
        ball_to_check_1.dx, ball_to_check_1.dy = -sin_a, -cos_a
        if self.dx == 0:
            ball_to_check_1.pulse = abs(cos_a / self.dy) * self.pulse
        else:
            ball_to_check_1.pulse = abs(sin_a / self.dx) * self.pulse

        dx = self.x - ball_to_check_2.x
        dy = self.y - ball_to_check_2.y
        d = vector_length(dx, dy)
        sin_a = dx / d
        cos_a = dy / d
        ball_to_check_2.dx, ball_to_check_2.dy = -sin_a, -cos_a
        if self.dx == 0:
            ball_to_check_2.pulse = abs(cos_a / self.dy) * self.pulse
        else:
            ball_to_check_2.pulse = abs(sin_a / self.dx) * self.pulse

        self.pulse = 0
        self.dx, self.dy = 0, 0

    def move(self, g, step_coefficient):
        v_x = self.pulse * self.dx - 5 / 2 * self.pulseSpin * self.spin[0]
        v_y = self.pulse * self.dy - 5 / 2 * self.pulseSpin * self.spin[1]
        v_absolute = vector_length(v_x, v_y)

        if self.pulseSpin != 0:
            cos_a = -(self.dx * self.pulse - 5 / 2 * self.spin[0] * self.pulseSpin) / v_absolute
            cos_b = -(self.dy * self.pulse - 5 / 2 * self.spin[1] * self.pulseSpin) / v_absolute
            spin_x = self.cloth_friction * g * cos_a / 2
            spin_y = self.cloth_friction * g * cos_b / 2
        else:
            spin_x = 0
            spin_y = 0

        # print(spin_x, self.dx)
        # print(spin_y, self.dy)
        # print(self.pulseSpin, self.pulse)
        # import os
        # os._exit(0)

        dx_guess = (self.dx * self.pulse + spin_x * self.pulseSpin) / step_coefficient
        dy_guess = (self.dy * self.pulse + spin_y * self.pulseSpin) / step_coefficient

        self.x_guess = self.x + dx_guess
        self.y_guess = self.y + dy_guess

    def check_ball_hit(self, balls):
        balls_to_check = []
        collided_balls_counter = 0
        for ball_to_check in balls:
            if self == ball_to_check:
                continue

            if is_balls_collided(self, ball_to_check):
                collided_balls_counter += 1
                self.update_guess_coordinates()
                ball_to_check.update_guess_coordinates()
                balls_to_check.append(ball_to_check)

        if collided_balls_counter == 0:
            pass
        elif collided_balls_counter == 1:
            self.hit_ball_by_ball(balls_to_check[0])
        elif collided_balls_counter == 2:
            self.hit_ball_by_ballx2(balls_to_check[0], balls_to_check[1])
        else:
            print('ERROR in checkBallHit, K>2.K=', collided_balls_counter)

    def check_board_hit(self, board):
        if (
            self.x_guess < self.radius or
            (self.x_guess > board.wide - self.radius)
        ):
            self.dx = -self.dx
            self.pulse *= board.loss
            self.pulseSpin *= board.loss + self.board_friction
        if (
            self.y_guess < self.radius or
            (self.y_guess > board.height - self.radius)
        ):
            self.dy = -self.dy
            self.pulse *= board.loss
            self.pulseSpin *= board.loss + self.board_friction

    def update_pulse(self, dir_summ_x, dir_summ_y, initial_pulse):
        self.pulse = abs(
            dir_summ_x * self.dx + dir_summ_y * self.dy) * initial_pulse

    def update_guess_coordinates(self):
        self.x_guess = self.x
        self.y_guess = self.y

    def update_coordinates(self):
        self.x = self.x_guess
        self.y = self.y_guess

    def paint_spin(self, field):
        if self.spin_item:
            field.delete(self.spin_item)

        self.spin_item = field.create_line(
            self.x, self.y,
            self.x + self.spin[0]*20, self.y + self.spin[1]*20,
            fill='black'
        )

    def paint_direction(self, field):
        if self.direction_item:
            field.delete(self.direction_item)

        self.direction_item = field.create_line(
            self.x, self.y,
            self.x + self.dx*20, self.y + self.dy*20,
            fill='red'
        )

    def paint_route(self, field):
        self.route_item = field.create_line(
            self.x, self.y,
            self.x+1, self.y+1,
            fill=self.color
        )

    def paint(self, field):
        if self.item:
            self.erase(field)

        self.item = field.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=self.color, outline=self.color
        )

        # self.paint_direction(field)
        # self.paint_spin(field)
        self.paint_route(field)

    def erase(self, field):
        field.delete(self.item)


def generate_balls():
    balls = list()
    delta_x = 0
    for i in range(1, 6):
        for j in range(i):
            balls.append(
                Ball(x=178 + j * 10 - delta_x, y=178 - i * 10, color='red'))

        delta_x += 5

    balls.append(Ball(x=178, y=65, color='black'))
    balls.append(Ball(x=178, y=178, color='hot pink'))
    balls.append(Ball(x=178, y=356, color='blue'))
    balls.append(Ball(x=120, y=565, color='green'))
    balls.append(Ball(x=178, y=565, color='sienna'))
    balls.append(Ball(x=236, y=565, color='yellow'))
    balls.append(Ball(x=0, y=0, color='white'))

    return balls


def is_balls_collided(ball_1, ball_2):
    distance = vector_length(
        ball_1.x_guess - ball_2.x, ball_1.y_guess - ball_2.y)
    distance_guess = vector_length(
        ball_1.x_guess - ball_2.x_guess, ball_1.y_guess - ball_2.y_guess)
    collision_distance = ball_1.radius + ball_2.radius

    if distance <= collision_distance or distance_guess <= collision_distance:
        return True
    else:
        return False
