import time
from threading import Thread
from tkinter import messagebox, Tk, IntVar, Entry, Canvas, END, Button

from Ball import generate_balls, BallField
from Board import Board
from Stick import Stick


STEP_COEFFICIENT = 1000
IS_HIT_HOLD = False
IS_STICK_HOLD = False
BOARD = Board(canvas=Canvas)
BALL_FRAME = BallField(canvas=Canvas, board_wide=BOARD.wide)
STICK = Stick()
BALLS = generate_balls()

ROOT_FRAME = Tk()
ROOT_FRAME.resizable(False, False)
ROOT_FRAME.geometry('{}x{}+0+20'.format(BOARD.wide + 501, BOARD.height + 202))

FORCE_ENTRY = Entry(ROOT_FRAME, textvariable=IntVar(value=100))
FORCE_ENTRY.place(x=BOARD.wide + 200, y=450, width=100, height=20)

BALL_FRAME.paint(ROOT_FRAME)
BOARD.paint(ROOT_FRAME)
BOARD.paint_balls(BALLS)


# MAKE LIST OF BALLS FINISH
# SIMPLE THINGS START
def push_stick():
    global IS_STICK_HOLD, IS_HIT_HOLD
    global STICK, BOARD, BALLS
    global STEP_COEFFICIENT
    global BALL_FRAME

    force_min = 0
    force_max = 1000

    try:
        force_value = float(FORCE_ENTRY.get())
    except ValueError:
        FORCE_ENTRY.delete(0, END)
        FORCE_ENTRY.insert(0, 0)
        messagebox.showinfo('Oops', 'Force value not digit')
        return

    if force_value < force_min or force_value > force_max:
        messagebox.showinfo(
            'Oops', 'Force value not between {} and {}'.format(
                force_min, force_max
            )
        )
        FORCE_ENTRY.delete(0, END)
        FORCE_ENTRY.insert(0, 0)
        return

    if not IS_STICK_HOLD or not IS_HIT_HOLD:
        messagebox.showinfo('Oops', 'Hold hit and stick first')
        return

    ball = STICK.stick_hit_ball(BOARD, BALLS, STEP_COEFFICIENT)

    if ball is None:
        messagebox.showinfo('Oops', 'Not hit any ball')
        return

    good_hit = STICK.hit_ball_by_stick(ball, force_value, BALL_FRAME)

    if not good_hit:
        messagebox.showinfo('Oops', 'Bad hit:a>0.6')
        return

    move_thread = Thread(target=check_timer)
    move_thread.setDaemon(True)
    move_thread.start()


def check_timer():
    global STEP_COEFFICIENT
    global BALLS, BOARD

    flag = True
    minimum_pulse = 1 / STEP_COEFFICIENT
    while flag:
        zero_pulse_balls = 0
        number_of_steps = STEP_COEFFICIENT / 10
        while number_of_steps > 0:

            for ball in BALLS:
                if max(ball.pulse, ball.pulseSpin) > minimum_pulse:
                    zero_pulse_balls = 0
                    ball.move(BOARD.g, STEP_COEFFICIENT)
                    ball.check_ball_hit(BALLS)
                    ball.check_board_hit(BOARD)
                    if number_of_steps == 1:
                        ball.pulse *= (1 - ball.board_friction) ** 2
                        ball.pulseSpin *= (1 - ball.cloth_friction) ** 2
                else:
                    zero_pulse_balls += 1
                    ball.pulse = 0
                    ball.pulseSpin = 0

                dx = abs(int(ball.x) - int(ball.x_guess))
                dy = abs(int(ball.y) - int(ball.y_guess))
                ball.update_coordinates()
                if dx > 0 or dy > 0:
                    ball.paint(BOARD.item)

            time.sleep(1 / STEP_COEFFICIENT)
            number_of_steps -= 1

            if zero_pulse_balls > len(BALLS):
                messagebox.showinfo('Oops', 'OK.Ready to next push!')
                return


# CALCULATIONS FINISH
# EVENTS START
def mouse_motion_main_field(event):
    global IS_HIT_HOLD, IS_STICK_HOLD
    global STICK, BOARD

    if not IS_HIT_HOLD:
        return

    if not IS_STICK_HOLD:
        STICK.calculate_back_coordinates(event.x, event.y)
        STICK.paint(BOARD.item)


def click_left_ball_field(event):
    global BALL_FRAME

    BALL_FRAME.item.delete(BALL_FRAME.point_of_hit)
    BALL_FRAME.item.delete(BALL_FRAME.rotation_axle)
    x = event.x
    y = event.y
    BALL_FRAME.point_of_hit = BALL_FRAME.item.create_oval(
        x - 20, y - 20, x + 20, y + 20, fill='red', outline='red')
    BALL_FRAME.coordinates = [x, y]


def click_left_main_field(event):
    global IS_HIT_HOLD, IS_STICK_HOLD
    global BOARD, BALLS, STICK

    if IS_HIT_HOLD:
        if not IS_STICK_HOLD:
            STICK.head = [event.x, event.y]
            STICK.calculate_back_coordinates(STICK.tail[0], STICK.tail[0])
            STICK.paint(BOARD.item)
        else:
            IS_STICK_HOLD = False
            click_left_main_field(event)
    else:
        BALLS[-1].x, BALLS[-1].y = event.x, event.y
        BALLS[-1].update_guess_coordinates()
        BALLS[-1].paint(BOARD.item)


def click_right_main_field(event):
    global IS_STICK_HOLD, IS_HIT_HOLD
    global BOARD, STICK

    if IS_HIT_HOLD:
        if not IS_STICK_HOLD:
            IS_STICK_HOLD = True
            STICK.paint(BOARD.item)
        else:
            IS_STICK_HOLD = False
            click_left_main_field(event)
    else:
        messagebox.showinfo('Oops', 'Place hit ball first')


def place_hit():
    global IS_HIT_HOLD
    IS_HIT_HOLD = False


def hold_hit():
    global IS_HIT_HOLD
    IS_HIT_HOLD = True


def place_stick():
    global IS_STICK_HOLD
    IS_STICK_HOLD = False


def hold_stick():
    global IS_STICK_HOLD
    IS_STICK_HOLD = True
# EVENTS FINISH
# BINDS
BOARD.item.bind('<Motion>', mouse_motion_main_field)
BOARD.item.bind('<Button-1>', click_left_main_field)
BOARD.item.bind('<Button-3>', click_right_main_field)

BALL_FRAME.item.bind('<Button-1>', click_left_ball_field)
###########################
# BUTTONS
# buttHoldHit = Button(ROOT_FRAME, text='Hold hit', command=hold_hit)
buttHoldHit = Button(ROOT_FRAME, text='Hold hit', command=hold_hit)
buttHoldHit.place(x=BOARD.wide + 200, y=344, width=100, height=20)

buttHoldStick = Button(ROOT_FRAME, text='Hold stick', command=hold_stick)
buttHoldStick.place(x=BOARD.wide + 200, y=366, width=100, height=20)

buttPlaceHit = Button(ROOT_FRAME, text='Place hit', command=place_hit)
buttPlaceHit.place(x=BOARD.wide + 200, y=300, width=100, height=20)

buttPlaceStick = Button(ROOT_FRAME, text='Place stick', command=place_stick)
buttPlaceStick.place(x=BOARD.wide + 200, y=322, width=100, height=20)

buttPushStick = Button(ROOT_FRAME, text='Push stick', command=push_stick)
buttPushStick.place(x=BOARD.wide + 200, y=388, width=100, height=20)
###########################
# PROGRAM START

ROOT_FRAME.mainloop()
