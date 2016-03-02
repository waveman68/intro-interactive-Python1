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

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
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
        self.cards = []  # create Hand object

    def __str__(self):
        return_string = 'Hand contains '
        for i in range(len(self.cards)):
            my_card = self.cards[i]
            return_string += str(my_card) + ' '
        # return a string representation of a hand
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
        pass  # draw a hand on the canvas, use the draw method for cards


# define deck class
class Deck:
    def __init__(self):
        self.card_deck = []
        for a_suit in SUITS:
            for a_rank in RANKS:
                self.card_deck.append(Card(a_suit, a_rank))
        pass  # create a Deck object

    def __str__(self):
        return_string = 'Deck contains '
        for i in range(len(self.card_deck)):
            my_card = self.card_deck[i]
            return_string += str(my_card) + ' '
        # return a string representation of a hand
        return return_string

    def shuffle(self):
        random.shuffle(self.card_deck)

    def deal_card(self):
        return self.card_deck.pop(-1)  # deal a card object from the deck


# define event handlers for buttons
def deal():
    global outcome, in_play
    global player_hand, dealer_hand, current_deck

    current_deck = Deck()
    current_deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    for i in range(0, 2):
        player_hand.add_card(current_deck.deal_card())
        dealer_hand.add_card(current_deck.deal_card())

    player_msg = 'Player hand is: ' + str(player_hand)
    dealer_msg = 'Dealer hand is: ' + str(dealer_hand)
    print(player_msg)
    print(dealer_msg)

    in_play = True


def hit():
    global player_hand, current_deck, in_play

    # if the hand is in play, hit the player
    if in_play and player_hand.get_value() <= 21:
        player_hand.add_card(current_deck.deal_card())

    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        print('You have busted.')
        in_play = False
    else:
        player_msg = 'Player hand is: ' + str(player_hand)
        print(player_msg)


def stand():
    global dealer_hand, player_hand, current_deck

    player_value = player_hand.get_value()
    print(player_value)
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(current_deck.deal_card())
    dealer_value = dealer_hand.get_value()
    print(dealer_value)

    dealer_msg = 'Dealer hand is: ' + str(dealer_hand)
    print(dealer_msg)

    # assign a message to outcome, update in_play and score
    if player_value > 21:
        print('You have busted, the dealer wins')
    elif player_value <= dealer_value:
        print('Dealer wins.')
    elif dealer_value > 21:
        print('The dealer has busted, the player wins')
    else:
        print('The player wins.')


# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below

    card = Card("S", "A")
    card.draw(canvas, [300, 300])


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


# remember to review the gradic rubric
