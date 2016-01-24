__author__ = 'Sam Broderick'

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math


# ================== 1 Initialize global variables =============
# ================== 2	Define helper functions ================

# helper function to start and restart the game
def new_game(high):
    # initialize global variables used in your code here
    global guessInt
    global secret_number
    global limit

    guessInt = 0                                # initialize
    secret_number = random.randrange(0, high)
    limit = high + 1                            # high - low + 1
    limit = math.ceil(math.log(limit, 2))       # log base 2

    print('New game. Guess a number in the interval  [0, %d).' % high)
    print('You have %d guesses.' % limit)

    return

# ================== 3 Define classes - no classes =============

# ================== 4 Define event handlers ===================
# define event handlers for control panel


def range100():
    # button that changes the range to [0,100) and starts a new game

    new_game(100)                              # reset game to [0, 100]

    return



def range1000():
    # button that changes the range to [0,1000) and starts a new game

    new_game(1000)                              # reset game to [0, 100]

    return

def input_guess(guess):
    # main game logic goes here
    global guessInt
    global secret_number
    guessInt = int(guess)
    print('Guess was %d' % guessInt)

    difference = secret_number - guessInt

    if difference == 0:
        print('Correct')
    elif difference > 0:
        print('Higher')
    elif difference < 0:
        print('Lower')
    else:
        print('error')

    return guessInt


# ================== 5 Create frame =============================

frame = simplegui.create_frame('Guess the Number', 200, 200)

inp = frame.add_input('Input guess', input_guess, 100)

button1 = frame.add_button('Range is [0,100)', range100, 100)
button2 = frame.add_button('Range is [0,1000)', range1000, 100)

# ================== 6 Register event handlers ==================
# register event handlers for control elements and start frame


# ================== 7 Start frame and timers ==================
# call new_game
new_game(100)                               # first game always with 100

# ================== 8 Testing =================================
secret_number = 74
input_guess("50")
input_guess("75")
input_guess("62")
input_guess("68")
input_guess("71")
input_guess("73")
input_guess("74")

range1000()
secret_number = 373
input_guess("500")
input_guess("250")
input_guess("313")
input_guess("344")
input_guess("359")
input_guess("367")
input_guess("371")


# always remember to check your completed program against the grading rubric
