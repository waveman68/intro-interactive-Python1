__author__ = 'Sam Broderick'

import simplegui

# Initialize globals
WIDTH = 600
HEIGHT = 400
time = 0

point_pos = [WIDTH / 2, HEIGHT / 2]
vel = [1, 0.7]
acc = [.1, .1]


# define event handlers

def draw(canvas):
    global time
    canvas.draw_circle(point_pos, 2, 1, "Red")
    # Update ball position
    point_pos[0] += vel[0] * time / 1000
    point_pos[1] += vel[1] * time / 1000

    vel[0] += acc[0] * time / 1000
    vel[1] += acc[1] * time / 1000

    if time % 5000 == 0 and time != 0:
        acc[0] += 0.1
        acc[1] += 0.1

    canvas.draw_text(str(time), (500, 50), 36, 'White')
    time += 10

    pass


# create frame
frame = simplegui.create_frame("Velocity ball control", WIDTH, HEIGHT)

# register event handlers
frame.set_draw_handler(draw)
frame.set_canvas_background('Black')

# start frame
frame.start()
