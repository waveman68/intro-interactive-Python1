# Testing template for the Hand class


import random

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (card_size[0] * (0.5 + RANKS.index(self.rank)), card_size[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, card_size, [pos[0] + card_size[0] / 2, pos[1] + card_size[1] / 2],
                          card_size)


#####################################################
# Student should insert code for Hand class here

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


###################################################
# Test code

c1 = Card("S", "A")
c2 = Card("C", "2")
c3 = Card("D", "T")
print(c1, c2, c3)
print(type(c1), type(c2), type(c3))

test_hand = Hand()
print(test_hand)

test_hand.add_card(c1)
print(test_hand)

test_hand.add_card(c2)
print(test_hand)

test_hand.add_card(c3)
print(test_hand)

print(type(test_hand))


###################################################
# Output to console
# note that the string representation of a hand will
# vary based on how you implemented the __str__ method

# SA C2 DT
# <class '__main__.Card'> <class '__main__.Card'> <class '__main__.Card'>
# Hand contains
# Hand contains SA
# Hand contains SA C2
# Hand contains SA C2 DT
# <class '__main__.Hand'>
