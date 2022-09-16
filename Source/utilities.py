# utilities.py
#
# Miscellaneous functions used by the application.
import csv
from operator import truediv

from os import system, name, path

DATA_FOLDER = "./Data/"

def get_words(file_name):

    if not path.isfile(DATA_FOLDER + file_name): return []
    with open(DATA_FOLDER + file_name, mode = "r") as file:

        words = []
        csvFile = csv.reader(file)
        for word in csvFile: 
            words.append(word)

    return words[0]

def compute_frequencies(words):

    frequencies = { 'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 
                    'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 
                    'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 
                    'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0 }

    for word in words:
        for letter in word:
            frequencies[letter] += 1

    return frequencies

def has_duplicates(word):

    if len(word) == 1: return False

    letter = word[0]
    new_word = word[1:]
    if letter in new_word:
        return True
    else:
        return has_duplicates(new_word)

def get_word_score(word, frequencies):

    score = 0
    for letter in word:
        score += frequencies[letter]
    return score

def find_best(words, frequencies, consider_duplicates=True):

    best_word = '$$$$$'
    best_score = 0

    for word in words:
        score = get_word_score(word, frequencies)
        if not consider_duplicates:
            if has_duplicates(word): continue

        if score > best_score:
            best_score = score
            best_word = word

    return (best_word, best_score)