"""
File: Distant Skies (command handler)
Description: Handles commands given by the player.
Author: Kent Carrier
Email: kentbo0528@gmail.com
"""

import time


def num_choice(message, lower=0, upper=None):
    """
    Loops until the user inputs a valid integer choice.
    :param message: str, message sent to console
    :param lower: int, inclusive lower acceptable bound
    :param upper: int or NoneType, inclusive upper acceptable bound
    :return: integer user input
    """

    while True:
        slow_print(message, 1, False)
        choice = input()
        try:
            choice = int(choice.strip())
        except ValueError:
            slow_print('Please input an integer.', 2)
            continue

        if upper is not None:
            if choice < lower or choice > upper:
                slow_print(('Please input between ', lower, ' and ', str(upper) + '.'), 2)
            else:
                return choice
        else:
            if choice < lower:
                slow_print('Please input a number above 0.', 2)
            else:
                return choice


def bool_choice(message, yes='y', no='n'):
    """
    Takes typed input and uses yes or no to return True or False
    :param message:
    :param yes: optional custom message that means "yes"
    :param no: optional custom message that means "no"
    :return:
    """

    while True:
        slow_print(message, 1, False)
        choice = input().strip()
        if choice is None or choice == '':
            slow_print('Please input "' + yes + '" or "' + no + '".', 2)
        elif choice[:len(yes)].lower() == yes:
            return True
        elif choice[:len(no)].lower() == no:
            return False
        else:
            slow_print('Please input "yes" or "no".', 2)


def list_choice(message, choices):
    """
    Allow the user to choose from a list of options.
    :param message: printed to the player with the input function
    :param choices: list of lowercase strings as potential choices
    :return: user's choice (str)
    """

    while True:

        slow_print(message, 1, False)
        choice = input().lower()
        print(choice)
        try:
            if isinstance(choices, list) or isinstance(choices, set):
                if choice not in choices:
                    if choice == 'help':
                        slow_print('Your choices are:')
                        for item in choices:
                            slow_print(item.capitalize())
                    elif bool_choice('Please choose from the options available. View options?'):
                        slow_print('Your choices are:')
                        try:
                            for item in choices:
                                if isinstance(item, str):
                                    slow_print(item.capitalize(), 2)
                                elif isinstance(item, int) or isinstance(item, float):
                                    slow_print(str(item), 2)
                                else:
                                    slow_print(item.name)
                        except AttributeError:
                            slow_print('An error has occurred accessing the list of options. Please contact Kent and '
                                       'tell him about this error and how you got it.')

                else:
                    return choice.strip()
            if isinstance(choices, dict):
                try:
                    choices.get(choice)
                    return choice.strip()
                except KeyError:
                    if choice == 'help':
                        slow_print('Your choices are:')
                        for item in choices.keys():
                            slow_print(item.capitalize())
                    elif bool_choice('Please choose from the options available. View options?'):
                        slow_print('Your choices are:')
                        try:
                            for item in choices.keys():
                                if isinstance(item, str):
                                    slow_print(item.capitalize(), 2)
                                elif isinstance(item, int) or isinstance(item, float):
                                    slow_print(str(item), 2)
                                else:
                                    slow_print(item.name)
                        except AttributeError:
                            slow_print(
                                'An error has occurred accessing the list of options. Please contact Kent and tell'
                                'him about this error and how you got it.')
        except TypeError:
            slow_print('Error found in input. Please re-enter your selection.')


def any_choice(message):

    while True:
        slow_print(message, 1, False)
        choice = input()
        if choice == '' or choice is None:
            slow_print('Do not leave the field blank.', 2)
        else:
            return choice.strip()


def slow_print(message, speed=1, new_line=True):

    for i in message:
        print(i, end='', flush=True)
        time.sleep(.05/(speed*(len(message)**.5)))
    if new_line:
        print('')
