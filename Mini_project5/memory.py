#!/usr/bin/env python
# -*- coding: latin-1 -*-

# code to use local simplegui simulator
try:
    import simplegui
    import codeskulptor

    SIMPLEGUICS2PYGAME = False
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    import SimpleGUICS2Pygame.codeskulptor as codeskulptor

    SIMPLEGUICS2PYGAME = True
    import SimpleGUICS2Pygame.codeskulptor_lib as codeskulptor_lib
    import SimpleGUICS2Pygame.simplegui_lib as simplegui_lib

import random

__author__ = 'Sam Broderick'

# implementation of card game - Memory

cards = list(range(8))  # global list of cards to reduce computation
cards += cards  # concatenate 2 lists to ensure pairs
turns = 0  # initialize turn counter


# helper function to initialize globals

def new_game():
    """
    Initialize variables after reset or first start
    """
    global cards, exposed, hand, state
    global card_1, card_2, turns

    hand = cards[:]
    random.shuffle(hand)  # hand for the game

    exposed = 16 * [False]  # initialize uncovered cards
    card_1 = None
    card_2 = None
    turns = 0

    state = 0  # number of cards initially uncovered


# define event handlers
def mouseclick(pos):
    """
    Mouse click handler with game logic
    :param pos: x, y
    :type pos: tuple
    """
    global card_1, card_2, exposed, hand, state, turns

    card_clicked = pos[0] // 50
    change_state = (card_clicked != card_1 and card_clicked != card_2 and
                    exposed[card_clicked] == False)

    if change_state:
        if state == 0:
            card_1 = card_clicked
            exposed[card_1] = True
            state = 1  # 1 card exposed
        elif state == 1:
            card_2 = card_clicked
            exposed[card_2] = True
            turns += 1
            state = 2  # end of turn
        else:
            if hand[card_1] != hand[card_2]:
                exposed[card_1] = False
                exposed[card_2] = False
            card_1 = card_clicked
            exposed[card_1] = True
            card_2 = None
            state = 1


# cards are logically 50x100 pixels in size
def draw(canvas):
    """
    Draws the 16 cards or the underlying number depending on exposed
    :param canvas: Canvas object in frame
    """
    global hand, exposed, turns
    for i, card in enumerate(hand):
        if exposed[i]:
            canvas.draw_text(str(card), (50 * i + 10, 70), 64, 'White')
        else:
            canvas.draw_polygon([(50 * i, 0), (50 * (i + 1), 0),
                                 (50 * (i + 1), 98), (50 * i, 98)], 3, 'Gray', 'Green')
    label.set_text('Turns = ' + str(turns))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric

# 1 pt - The game correctly draws 16 cards on the canvas (horizontally).
# ===> check
# 1 pt - The cards appear in eight unique pairs.
# ===> check
# 1 pt - The game ignores clicks on exposed cards.
# ===> check

# 1 pt - At the start of the game, a click on a card exposes the card that
# was clicked on.
# ===> check
# 1 pt - If one unpaired card is exposed, a click on a second unexposed card
#  exposes the card that was clicked on.
# ===> check
# 1 pt - If two unpaired cards are exposed, a click on an unexposed card
# exposes the card that was clicked on and flips the two unpaired cards over.
# ===> check

# 1 pt - If all exposed cards are paired, a click on an unexposed card
# exposes the card that was clicked on and does not flip any other cards.
#  ===> check
# 1 pt - Cards paired by two clicks in the same turn remain exposed until the
# start of the next game.
#  ===> check
# 1 pt - The game correctly updates and displays the number of turns in the
# current game in a label displayed in the control area. The counter may be
# incremented after either the first or second card is flipped during a turn.
#  ===> check

# 1 pt - The game includes a "Reset" button that resets the turn counter and
# restarts the game.
#  ===> check
# 1 pt - The deck is also randomly shuffled each time the "Reset" button is
# pressed, so that the cards are in a different order each game.
#  ===> check
