__author__ = 'Sam Broderick'

import simplegui

# Initialize globals
WIDTH = 300
HEIGHT = 200

point_pos = [10, 20]
vel = [3, 0.7]


# define event handlers
def draw(canvas):
    canvas.draw_circle(point_pos, 2, 1, "Red")
    # Update ball position
    point_pos[0] += vel[0]
    point_pos[1] += vel[1]

    canvas.draw_polygon([(50, 50), (180, 50), (180, 140), (50, 150)], 5, 'Blue', 'White')


# def keydown(key):
#     acc = 1
#     if key==simplegui.KEY_MAP["left"]:
#         vel[0] -= acc
#     elif key==simplegui.KEY_MAP["right"]:
#         vel[0] += acc
#     elif key==simplegui.KEY_MAP["down"]:
#         vel[1] += acc
#     elif key==simplegui.KEY_MAP["up"]:
#         vel[1] -= acc
#
#     print point_pos

# create frame
frame = simplegui.create_frame("Velocity ball control", WIDTH, HEIGHT)

# register event handlers
frame.set_draw_handler(draw)
# frame.set_keydown_handler(keydown)

# start frame
frame.start()
