__author__ = 'Sam Broderick'

# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0  # time in tenths of seconds
attemps = 0
successes = 0
running = False


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """
    This function formats an integer t, number of tenths of seconds in a digital
    stop watch format
    :param t: int - time in
    :return: str
    """
    tenths = t % 10
    seconds = (t // 10) % 60
    minutes = (t // 10) // 60
    if seconds < 10:
        seconds_str = '0' + str(seconds)
    else:
        seconds_str = str(seconds)
    t_string = str(minutes) + ':' + seconds_str + '.' + str(tenths)
    return t_string


# define event handlers for buttons; "Start", "Stop", "Reset"
def button_handler1():  # Start button
    global running
    timer.start()
    running = True


def button_handler2():  # Stop button
    global running
    global attemps
    global successes
    timer.stop()
    if running == True:
        attemps += 1
        if time % 10 == 0:
            successes += 1
    running = False


def button_handler3():  # Reset button
    global time
    global running
    global attemps
    global successes
    timer.stop()
    running = False
    time = 0  # reset all global ints to 0
    attemps = 0
    successes = 0


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1
    pass


# define draw handler
def draw_handler(canvas):
    global time
    if time < 3600:
        message = format(time)
    else:
        message = '1 hour! Please stop!!'
    canvas.draw_text(message, (110, 110), 48, 'White')
    success_rate = str(successes) + '/' + str(attemps)
    canvas.draw_text(success_rate, (260, 30), 24, 'Green')


# create frame
frame = simplegui.create_frame('Stopwatch: The Game', 300, 200, 100)
frame.set_canvas_background('Black')
frame.set_draw_handler(draw_handler)

button1 = frame.add_button('Start', button_handler1, 50)
button2 = frame.add_button('Stop', button_handler2, 50)
button2 = frame.add_button('Reset', button_handler3, 50)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()


# Please remember to review the grading rubric

# 1. 1 pt - The program successfully opens a frame with the stopwatch stopped. CHECK
# 2. 1 pt - The program has a working "Start" button that starts the timer. CHECK
# 3. 1 pt - The program has a working "Stop" button that stops the timer. CHECK
# 4. 1 pt - The program has a working "Reset" button that stops the timer (if running) and resets the timer to 0. CHECK
# 5. 4 pts - The time is formatted according to the description in step 4 above. CHECK
# 6. 2 pts - The program correctly draws the number of successful stops at a whole second vs. the total number of stops.
#     CHECK
# 7. 2 pts - The "Stop" button correctly updates these success/attempts numbers.CHECK
# 8. 1 pt - The "Reset" button clears the success/attempts numbers. CHECK
