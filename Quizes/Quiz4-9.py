__author__ = 'Sam Broderick'

import simplegui

# Initialize globals
WIDTH = 300
HEIGHT = 200

x = 5
n = 0


# define event handlers
def draw(canvas):
    canvas.draw_text(str(n), (250, 50), 24, 'White')
    canvas.draw_text(str(n), (130, 100), 36, 'Green')


def keydown(key):
    global x
    global n

    x *= 2
    n += 1
    print('Iteration %d, key down x is: %d' % (n, x))


def keyup(key):
    global x
    x -= 3
    print('Iteration %d, key down x is: %d' % (n, x))


# create frame
frame = simplegui.create_frame("Key driven calculation", WIDTH, HEIGHT)

# register event handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

# start frame
frame.start()
