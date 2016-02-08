__author__ = 'Sam Broderick'


import simplegui

# global state

result = 0
iteration = 0

# helper functions

def init(start):
    """
    Initializes global parameter n
    :param start:
    """
    global result
    result = start
    print
    "Input is", result

def get_next(current):
    """
    Calculation for Collatz conjecture
    :param current: int
    :return: int
    """
    print(current)
    if current % 2 == 0:
        return_value = current / 2
    elif current % 2 == 1:
        return_value = current * 3 + 1
    else:
        return_value = None
    return return_value

# timer callback

def update():
    """
    Timer update function to iterate Collatz conjecture
    """
    global iteration, result
    iteration += 1
    # Stop iterating if result is 1
    if result == 1:
        timer.stop()
        print "Output is", result
    else:
        result = get_next(result)

# register event handlers

timer = simplegui.create_timer(1, update)

# start program
init(23)
timer.start()
