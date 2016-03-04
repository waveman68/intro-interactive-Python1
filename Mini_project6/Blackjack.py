# Mini-project #6 - Blackjack


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
# card class and class/function structure from class

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ''
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        # create Hand object with list cards
        self.cards = []

    def __str__(self):
        return_string = 'Hand contains'

        # iterate through card objects and append card strings
        for i in range(len(self.cards)):
            # prepend space, better for split method
            return_string += ' ' + str(self.cards[i])

        # return a string representation of the hand
        return return_string

    def add_card(self, card):
        self.cards.append(card)  # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value
        # if it doesn't bust
        value_list = []
        for a_card in self.cards:
            value = VALUES[a_card.get_rank()]
            value_list.append(value)

        # compute the value of the hand, see Blackjack video
        value = sum(value_list)
        if 1 in value_list and value + 10 <= 21:
            return value + 10
        else:
            return value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards

        # iterate through card objects and use draw method with 1/4 card space
        for idx in range(len(self.cards)):
            self.cards[idx].draw(canvas, [pos[0] + idx * int(1.25 * CARD_SIZE[0]),
                                          pos[1]])


# define deck class
class Deck:
    def __init__(self):
        self.card_deck = []  # create a deck

        # fill the deck
        for a_suit in SUITS:
            for a_rank in RANKS:
                self.card_deck.append(Card(a_suit, a_rank))

    def __str__(self):
        # return a string representation of a hand
        return_string = 'Deck contains'
        for i in range(len(self.card_deck)):
            # prepend space, better for split method
            return_string += ' ' + str(self.card_deck[i])
        return return_string

    def shuffle(self):
        random.shuffle(self.card_deck)

    def deal_card(self):
        return self.card_deck.pop(-1)  # deal a card object from the deck


# define event handlers for buttons
def deal():
    global outcome, in_play, score
    global player_hand, dealer_hand, current_deck

    # if deal interrupts a hand, than player loses
    if in_play:
        outcome = 'The dealer wins'
        score -= 1
    else:
        outcome = ''  # clears result
    current_deck = Deck()  # always a new deck per class
    current_deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    for i in range(0, 2):
        player_hand.add_card(current_deck.deal_card())
        dealer_hand.add_card(current_deck.deal_card())

    in_play = True


def hit():
    global player_hand, current_deck, in_play, outcome, score

    # if the hand is in play, hit the player
    if in_play and player_hand.get_value() <= 21:
        player_hand.add_card(current_deck.deal_card())

    outcome = ''

    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        in_play = False
        stand()
        outcome = 'The dealer wins.'
        score -= 1


def stand():
    global dealer_hand, player_hand, current_deck
    global in_play, outcome, score

    player_value = player_hand.get_value()
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(current_deck.deal_card())
        dealer_value = dealer_hand.get_value()

        # assign a message to outcome, update in_play and score
        if player_value > 21:
            outcome = 'The dealer wins'
            score -= 1
        elif player_value <= dealer_value and dealer_value <= 21:
            outcome = 'The dealer wins.'
            score -= 1
        elif dealer_value > 21:
            outcome = 'The player wins'
            score += 1
        else:
            outcome = 'The player wins.'
            score += 1

    in_play = False


# draw handler
def draw(canvas):
    global player_hand, dealer_hand, in_play, outcome, score

    # draw basic text
    canvas.draw_text('Blackjack', (100, 100), 48, 'Red', 'sans-serif')
    canvas.draw_text('Score: ' + str(score), (350, 100), 36, 'Black')
    canvas.draw_text('Dealer', (100, 160), 36, 'Black')
    canvas.draw_text('Player', (100, 360), 36, 'Black')

    # draw cards
    dealer_hand.draw(canvas, (100, 200))
    player_hand.draw(canvas, (100, 400))

    # draw messages and cover dealer's hole card
    if in_play:
        canvas.draw_text('Hit or stand?', (300, 360), 36, 'Black')
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_SIZE,
                          [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]],
                          CARD_BACK_SIZE)
    else:
        canvas.draw_text('New deal?', (300, 360), 36, 'Black')
    canvas.draw_text(outcome, (300, 160), 36, 'Black')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()


# remember to review the grading rubric

# The program displays the title "Blackjack" on the canvas.
# 1 pt - check

# The program displays 3 buttons ("Deal", "Hit" & "Stand") in control area.
# 1 pt - check

# The program graphically displays the player's hand using card images.
# (1 pt if text is displayed in the console instead)
# 2 pts - check
# The program graphically displays the dealer's hand using card images.
# Displaying both of the dealer's cards face up is allowable when evaluating
# this bullet. (1 pt if text displayed in the console instead)
# 2 pts -  check

# The dealer's hole card is hidden until the current round is over. After
# the round is over, it is displayed.
# 1 pt -  check

# Pressing the "Deal" button deals out two cards each to the player and
# dealer. (1 pt per player)
# 2 pts - check

# Pressing the "Deal" button in the middle of the round causes the player to
# lose the current round.
# 1 pt - check

# Pressing the "Hit" button deals another card to the player.
# 1 pt - check

# Pressing the "Stand" button deals cards to the dealer as necessary.
# 1 pt - check

# The program correctly recognizes the player busting.
# 1 pt - check

# The program correctly recognizes the dealer busting.
# 1 pt - check

# The program correctly computes hand values and declares a winner. Evaluate
# based on messages.
# 1 pt - check

# The program accurately prompts the player for an action with messages
# similar to "Hit or stand?" and "New deal?". (1 pt per message)
# 2 pts -  check

# The program implements a scoring system that correctly reflects wins
# and losses. Please be generous in evaluating this item.
# 1 pt - check
