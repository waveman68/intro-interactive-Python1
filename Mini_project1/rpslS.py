# Rock-paper-scissors-lizard-Spock template

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random


# helper functions

# Note to graders. The """Docstring""" is an official Python format to provide help
# on the function. It makes a statement about the function, what it returns and what
# it takes as parameters.


def name_to_number(name):
    """
    Returns the number associated with the name.

     :rtype: int
     :param name: str
    """

    # convert name to number using if/elif/else
    # don't forget to return the result!
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        return 'error'


def number_to_name(number):
    """
    Returns the number associated with the name.

     :rtype: str
     :param number: int
    """

    # convert number to a name using if/elif/else
    # don't forget to return the result!
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        return 'error'


def rpsls(player_choice):
    """
    Accepts the player choice as a string, generates a random computer choice.
    Uses modulo rules to determine the winner.

     :rtype: None
     :param player_choice: str
    """

    # print a blank line to separate consecutive games
    print(''+ '\n')

    # print out the message for the player's choice
    print('Player chooses ' + player_choice+ '\n')

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)

    # print out the message for computer's choice
    print('Computer chooses ' + comp_choice+ '\n')

    # compute difference of comp_number and player_number modulo five
    difference = (comp_number - player_number) % 5

    # use if/elif/else to determine winner, print winner message
    if difference == 0:
        print('Player and computer tie!')	# \n already in line 82
    elif difference > 2:
        print('Player wins!')
    elif difference <= 2:
        print('Computer wins!')
    else:
        print('error')

    return

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")


# always remember to check your completed program against the grading rubric

# valid CodeSkulptor URL
#

# implements function rpsls() and helper function name_to_number()
# True

# does not throw an error
# True

# Program prints blank lines between games
# True

# Program prints player choice correctly
# True

# Program prints computer choice correctly
# True

# Computer's guesses vary between five calls to rpsls() in each run of the program.
# True

# Computer's guesses vary between runs of the program.
# True

# Program prints outcome
# True

# Program chooses correct winner
# True
