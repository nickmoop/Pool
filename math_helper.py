import math


def calculate_ball_direction(dir_x, dir_y):
    if dir_y == 0:
        dir_ball_x = 0
    else:
        dir_ball_x = dir_x / dir_y

    if dir_x == 0:
        dir_ball_x = 1
        dir_ball_y = 0
    else:
        dir_ball_y = dir_y / dir_x

    distance = vector_length(dir_ball_x, dir_ball_y)
    if distance != 0:
        dir_ball_x = abs(dir_ball_x / distance)
        dir_ball_y = abs(dir_ball_y / distance)
    else:
        dir_ball_x = dir_y
        dir_ball_y = dir_x

    return [dir_ball_x, dir_ball_y]


def calculate_ball_sign(dir_summ_x, dir_summ_y, dir_x, dir_y):
    sign_summ_x = math.copysign(1, dir_summ_x)
    sign_summ_y = math.copysign(1, dir_summ_y)
    sign_x = math.copysign(1, dir_x)
    sign_y = math.copysign(1, dir_y)
    sign_ball_x = sign_summ_x
    sign_ball_y = sign_summ_y

    if sign_summ_x == sign_x and sign_summ_y == sign_y:
        if abs(dir_summ_x) < abs(dir_x):
            sign_ball_x = -sign_summ_x
        if abs(dir_summ_y) < abs(dir_y):
            sign_ball_y = -sign_summ_y

    return sign_ball_x, sign_ball_y


def vector_length(dx, dy):
    return (dx**2 + dy**2)**0.5
