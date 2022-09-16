# main.py
#
# This is a console application that displays the Wordle words

from operator import truediv
import os

from utilities import get_words
from utilities import compute_frequencies
from utilities import find_best

WORDLE_DATA = "UnquotedWords.txt"
QUITSTRING  = 'Q'

def has_letter(letter, word):

    return letter in word

def not_at (letter, word, position):

    return word[position] != letter

def is_at (letter, word, position):

    return word[position] == letter

def has_not (letter, word):

    return letter not in word

def do_not_ignore(guess, word, item):

    letter = word[item]
    letter_count = 0
    can_ignore = False

    for index in range(0, 5):
        if letter == word[index]:
            letter_count += 1
            if guess[index] in ['g', 'y']: can_ignore = True
            if (letter_count > 1) & can_ignore: return can_ignore

    return can_ignore

def check_this (function, result):

    return True if function & result else False

def is_good(word):

    # Use atone as the starting word

    result = has_letter('a', word)

    result = check_this ( has_letter('t', word), result )
    # result = check_this ( has_letter('o', word), result )
    # result = check_this ( has_letter('n', word), result )
    result = check_this ( has_letter('e', word), result )
    # result = check_this ( has_letter('i', word), result )
    # result = check_this ( has_letter('s', word), result )
    # result = check_this ( has_letter('h', word), result )
    # result = check_this ( has_letter('r', word), result )
    result = check_this ( has_letter('l', word), result )

    result = check_this ( not_at('a', word, 0), result )
    result = check_this ( not_at('t', word, 1), result )
    result = check_this ( not_at('e', word, 4), result )
    result = check_this ( not_at('a', word, 1), result )
    result = check_this ( not_at('t', word, 2), result )
    result = check_this ( not_at('e', word, 3), result )
    result = check_this ( not_at('t', word, 0), result )
    # result = check_this ( not_at('s', word, 4), result )
    # result = check_this ( not_at('o', word, 2), result )

    result = check_this ( is_at('l', word, 1), result )
    result = check_this ( is_at('e', word, 2), result )
    result = check_this ( is_at('a', word, 3), result )
    result = check_this ( is_at('t', word, 4), result )

    result = check_this ( has_not('n', word), result )
    # result = check_this ( has_not('t', word), result )
    result = check_this ( has_not('h', word), result )
    result = check_this ( has_not('o', word), result )
    result = check_this ( has_not('s', word), result )
    # result = check_this ( has_not('e', word), result )
    result = check_this ( has_not('r', word), result )
    result = check_this ( has_not('d', word), result )
    result = check_this ( has_not('c', word), result )

    return result

def word_passes(word, guess, wordle_result):

    for item in range(0, 5):
        if wordle_result[item].lower() == 'r':
            if not has_not(guess[item], word): return False
        if wordle_result[item].lower() == 'y':
            if not has_letter(guess[item], word): return False
            if not not_at(guess[item], word, item): return False
        if wordle_result[item].lower() == 'g':
            if do_not_ignore(guess, word, item):
                if not is_at(guess[item], word, item): return False
    
    return True

def check_result(words, guess, result):

    words_that_pass = []    
    for word in words:
        if word_passes(word, guess, result): words_that_pass.append(word)

    return words_that_pass

def is_rgy(input):

    for letter in input:
        if letter.lower() not in 'rgy': return False
    return True

def check_user_input(user_input):
    """ Validate the user's input

    checkUserInput will validate the user's input. This is a very redimentary
    validation method. It checks three things ...

    1. Checks the length of the input is five letters
    2. Checks the input only contains r g or y (or q to quit)
 
    Note: If the user enters 'Q', a minus one is returned to the caller.
    
    Args:
        userInput: A string entered by the user.
    
    Returns:
        A valid integer result.
    """

    if user_input.upper() == QUITSTRING: return QUITSTRING
    if len(user_input) != 5:
        print('\nThis is expected five letters like \'ggyrg\'')
        return get_user_input()
    if not is_rgy(user_input):
        print('\nThis only accepts the letters \'r\', \'g\', or \'y\' like \'ggyrg\'')
        return get_user_input()
    return user_input

def get_user_input(guess):
    """ Get user input from the console
    getUserInput is a simple method for reading from the console.

    Valid input is a string of five letters. The letters must be in the
    set { r, g, y } where 
    r means that the letter is not in the solution (grey)
    g means that the letter is in the proper position (green)
    y means that the letter is in the solution at a different position (yellow)

    example: ryggr
 
    Returns:
        A string that represents the user's input.
    """
    print('The guess is {word} please type it into wordle.'.format(word=guess))
    return check_user_input(input('What was Wordle\'s response? Or type \'Q\' to quit. '))

words = get_words(WORDLE_DATA)
frequencies = compute_frequencies(words)
# print('The starting word is {word}.'.format(word=find_best(words, frequencies, False)))

# count = 0
# for word in words:
#     if is_good(word): 
#         count += 1
#         print(word)

# print('{count} possible choices.'.format(count=count))

(guess, score) = find_best(words, frequencies, consider_duplicates=False)
wordle_result = get_user_input(guess)
while wordle_result != QUITSTRING:
    words = check_result(words, guess, wordle_result)
    (guess, score) = find_best(words, frequencies)
    wordle_result = get_user_input(guess)
