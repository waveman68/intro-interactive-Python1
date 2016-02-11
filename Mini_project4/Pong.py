__author__ = 'Sam Broderick'

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = int(PAD_WIDTH / 2)
HALF_PAD_HEIGHT = int(PAD_HEIGHT / 2)
LEFT = False
RIGHT = True
X_MIDDLE = int(WIDTH / 2)
Y_MIDDLE = int(HEIGHT / 2)


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    """

    :type direction: object
    :param direction:
    """
    global ball_pos, ball_vel  # these are vectors stored as lists

    # Center ball
    ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]

    # Assign velocity
    if direction:
        x_velocity = random.randrange(3, 6)
    else:
        x_velocity = -random.randrange(3, 6)
    ball_vel = [x_velocity, -random.randrange(2, 6)]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    # put the paddles in the middle
    paddle1_pos = Y_MIDDLE
    paddle2_pos = Y_MIDDLE

    # initial paddle velocities zero
    paddle1_vel = 0
    paddle2_vel = 0

    seed_direction = random.choice([LEFT, RIGHT])
    spawn_ball(seed_direction)


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([X_MIDDLE, 0], [X_MIDDLE, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # collide and reflect off top/bottom walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # collide/reflect off paddle or re-spawn if ball reaches gutter

    # left wall means paddle 1
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        paddle_top = paddle1_pos - HALF_PAD_HEIGHT
        paddle_bottom = paddle1_pos + HALF_PAD_HEIGHT
        if paddle_top <= ball_pos[1] <= paddle_bottom:
            ball_vel[0] = -ball_vel[0]
        else:
            spawn_ball(RIGHT)
    # right wall is paddle 2
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        paddle_top = paddle2_pos - HALF_PAD_HEIGHT
        paddle_bottom = paddle2_pos + HALF_PAD_HEIGHT
        if paddle_top <= ball_pos[1] <= paddle_bottom:
            ball_vel[0] = -ball_vel[0]
        else:
            spawn_ball(LEFT)

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    # prevent paddles from moving beyond top/bottom walls
    # paddle 1
    if paddle1_pos <= HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT

    # paddle 2
    if paddle2_pos <= HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT

    # draw paddles
    x_pad1 = HALF_PAD_WIDTH
    canvas.draw_line((x_pad1, paddle1_pos + HALF_PAD_HEIGHT),
                     (x_pad1, paddle1_pos - HALF_PAD_HEIGHT),
                     PAD_WIDTH, 'Red')

    x_pad2 = WIDTH - HALF_PAD_WIDTH
    canvas.draw_line((x_pad2, paddle2_pos + HALF_PAD_HEIGHT),
                     (x_pad2, paddle2_pos - HALF_PAD_HEIGHT),
                     PAD_WIDTH, 'Green')

    # determine whether paddle and ball collide

    # draw scores


def keydown(key):
    global paddle1_vel, paddle2_vel

    # initialize paddle velocity
    pad_vel = 20

    # set paddle 1 velocity based on key movements
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -pad_vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = pad_vel

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -pad_vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = pad_vel


def keyup(key):
    global paddle1_vel, paddle2_vel

    # paddle 1 stops moving
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0

    # paddle 2 stops moving
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()
