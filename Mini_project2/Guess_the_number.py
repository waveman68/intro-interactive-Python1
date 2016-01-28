import simplegui
import random
import math

__author__ = 'Sam Broderick'

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

# ================== 1 Initialize global variables =============

global high
high = 100

# ================== 2	Define helper functions ================

# helper function to start and restart the game


def new_game():
    # initialize global variables used in your code here
    global guessInt
    global secret_number
    global limit
    global numberGuesses
    global high

    guessInt = 0                                # initialize
    numberGuesses = 0
    secret_number = random.randrange(0, high)
    limit = high + 1                            # high - low + 1
    limit = math.ceil(math.log(limit, 2))       # log base 2

    print('New game. Guess a number in the interval  [0, %d).' % high)
    print('You have %d guesses.' % limit)
    print('\n')

    return

# ================== 3 Define classes - no classes =============

# ================== 4 Define event handlers ===================
# define event handlers for control panel


def range100():
    # button that changes the range to [0,100) and starts a new game
    global high

    high = 100
    new_game()  # reset game to [0, 100]

    return


def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global high

    high = 1000
    new_game()  # reset game to [0, 100]

    return


def input_guess(guess):
    # main game logic goes here
    global guessInt
    global secret_number
    global limit
    global numberGuesses

    guessInt = int(guess)

    numberGuesses += 1
    print('Guess was %d. %d guesses left.' % (guessInt, limit - numberGuesses))
    difference = secret_number - guessInt

    if difference == 0:
        print('Correct')
        print('\n')
        new_game()
        return  # remainder of logic unnecessary
    elif difference > 0:
        print('Higher')
    elif difference < 0:
        print('Lower')
    else:
        print('error')

    if numberGuesses >= limit:
        print('No guesses left. You lose.' % limit)
        print('\n')
        new_game()

    return


# ================== 5 Create frame =============================

frame = simplegui.create_frame('Guess the Number', 200, 200)

inp = frame.add_input('Input guess', input_guess, 100)

button1 = frame.add_button('Range is [0,100)', range100, 100)
button2 = frame.add_button('Range is [0,1000)', range1000, 100)

# ================== 6 Register event handlers ==================
# register event handlers for control elements and start frame


# ================== 7 Start frame and timers ==================
# call new_game
new_game()  # first game always with 100

# ================== 8 Testing =================================

# === Check range 100 ===
secret_number = 74
input_guess("50")
input_guess("75")
input_guess("62")
input_guess("68")
input_guess("71")
input_guess("73")
input_guess("74")

# === Check guess limit ===
secret_number = 42
input_guess("1")
input_guess("2")
input_guess("3")
input_guess("4")
input_guess("5")
input_guess("6")

# === Check range 1000 ===
range1000()
secret_number = 373
input_guess("500")
input_guess("250")
input_guess("375")
input_guess("313")
input_guess("344")
input_guess("359")
input_guess("367")
input_guess("371")
input_guess("373")


# always remember to check your completed program against the grading rubric

# 1 pt — The game starts immediately: CHECKED.

# 1 pt — A game is always in progress. Finishing immediately starts another:
#        CHECKED.

# 1 pt — The game reads guess and correctly prints it out: CHECKED.

# 3 pts — Correctly plays “Guess the number” in [0, 100) and is understandable
#         3 games correct. 1 pt for each correct game: CHECKED.

# 2 pts — Includes two buttons to select [0, 100) or [0, 1000) for the secret
#         number.Buttons change range and print message. (1 pt / button.):
#         CHECKED.

# 2 pts — Game restricts player to finite number of guesses and terminates the
#         game when guesses exhausted. 1 pt if number of remaining guesses
#         is printed, but  game does not terminate correctly: CHECKED.

# 1 pt — Game varies number of guesses based on the range of the secret number —
#        seven guesses for [0, 100), ten guesses for [0, 1000): CHECKED.
