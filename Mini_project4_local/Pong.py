#!/usr/bin/env python
# -*- coding: latin-1 -*-
import math
import random

try:
    import simplegui

    SIMPLEGUICS2PYGAME = False
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    SIMPLEGUICS2PYGAME = True

__author__ = 'Sam Broderick'

# Implementation of classic arcade game Pong


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

    :rtype: object
    :type direction: object
    :param direction:
    """
    global ball_pos, ball_vel  # these are vectors stored as lists

    # Center ball
    ball_pos = [int(WIDTH / 2), int(HEIGHT / 2)]

    # Assign velocity, start slow
    if direction:
        x_velocity = random.randrange(3, 6)
    else:
        x_velocity = -random.randrange(3, 6)
    ball_vel = [x_velocity, -random.randrange(2, 6)]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    # reset scores
    score1 = 0
    score2 = 0

    # put the paddles in the middle
    paddle1_pos = Y_MIDDLE
    paddle2_pos = Y_MIDDLE

    # initial paddle velocities zero
    paddle1_vel = 0
    paddle2_vel = 0

    # generate a random direction and spawn a new ball
    seed_direction = random.choice([LEFT, RIGHT])
    spawn_ball(seed_direction)


def update_paddle(pad_pos, pad_vel):
    """
    Takes a paddle position and velocity and determines
    if the paddle is in bounds
    :rtype: int
    :type pad_pos: int
    :param pad_pos:
    :type pad_vel: int
    :param pad_vel:
    """
    # paddle in bounds
    if HALF_PAD_HEIGHT <= pad_pos + pad_vel <= HEIGHT - HALF_PAD_HEIGHT:
        return pad_pos + pad_vel
    # paddle is to high
    elif pad_pos + pad_vel < HALF_PAD_HEIGHT:
        return HALF_PAD_HEIGHT
    # paddle is too low
    elif HEIGHT - HALF_PAD_HEIGHT < pad_pos + pad_vel:
        return HEIGHT - HALF_PAD_HEIGHT


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

    # test if ball reaches left gutter and paddle 1 is there
    ball_at_paddle1 = (paddle1_pos - HALF_PAD_HEIGHT <=
                       ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT)
    ball_at_left_gutter = ball_pos[0] <= BALL_RADIUS + PAD_WIDTH

    # test if ball reaches left gutter and paddle 2 is there
    ball_at_paddle2 = (paddle2_pos - HALF_PAD_HEIGHT <=
                       ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT)
    ball_at_right_gutter = ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS

    if ball_at_left_gutter and not ball_at_paddle1:
        # paddle1 not there
        score2 += 1
        spawn_ball(RIGHT)
    elif ball_at_right_gutter and not ball_at_paddle2:
        # right wall is paddle 2
        score1 += 1
        spawn_ball(LEFT)

    # determine whether paddle and ball collide
    # determination already done for gutter code, reflect/speed up only
    if ((ball_at_paddle1 and ball_at_left_gutter) or
            (ball_at_paddle2 and ball_at_right_gutter)):
        # ceil ensures speed-up also for small velocities
        ball_vel = [-math.ceil(1.1 * x) for x in ball_vel]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # update paddle's vertical position, keep paddle on the screen
    # prevent paddles from moving beyond top/bottom walls via new function

    paddle1_pos = update_paddle(paddle1_pos, paddle1_vel)
    paddle2_pos = update_paddle(paddle2_pos, paddle2_vel)

    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT),
                     (HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),
                     PAD_WIDTH, 'Red')

    x_pad2 = WIDTH - HALF_PAD_WIDTH
    canvas.draw_line((x_pad2, paddle2_pos + HALF_PAD_HEIGHT),
                     (x_pad2, paddle2_pos - HALF_PAD_HEIGHT),
                     PAD_WIDTH, 'Green')

    # draw scores
    canvas.draw_text(str(score1), (150, 40), 36, 'Red')
    canvas.draw_text(str(score2), (450, 40), 36, 'Green')


def keydown(key):
    global paddle1_vel, paddle2_vel

    # initialize paddle velocity
    pad_vel = 10

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

# register event handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 50)

# start frame
new_game()
frame.start()

# 1 pt - Ball spawns in the middle of the canvas with either an upward left or an upward right velocity.
# Check

# 2 pts - Ball bounces off of the top and bottom walls correctly.
# Check

# 2 pts - Ball respawns in the middle of the screen when it strikes the left or right gutter but not the paddles.
# Check

# 1 pt - Left and right gutters (instead of the edges of the canvas) are properly used as the edges of the table.
# Check

# 1 pt - Ball spawns moving towards the player that won the last point.
# Check

# 2 pts - 'w' and 's' keys correctly control the velocity of the left paddle as described above.
# Check

# 2 pts - Up and down arrows keys correctly control the velocity of the right paddle as described above.
# Check

# 2 pts - Edge of each paddle is flush with the gutter. (1 pt per paddle)
# Check

# 2 pts - Paddles stay on the canvas at all times. (1 pt per paddle)
# Check

# 2 pts - Ball correctly bounces off the left and right paddles. (1 pt per paddle)
# Check

# 1 pt - Scoring text is positioned and updated appropriately. Positioning need only approximate that in the video.
# Check

# 1 pt - Game includes a "Restart" button that resets the score and relaunches Ball.
# Check
