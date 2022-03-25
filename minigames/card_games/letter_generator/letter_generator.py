import time
from copy import deepcopy
from timeit import timeit

from base.utility_functions import list_to_string
from minigames.card_games.letter_generator.utilities import get_letter_combinations, get_all_letter_combinations, \
    list_already_has_item, remove_duplicates

# Used for finding combinations of letters that produce enough words that the user could find one
# It will be pretty slow because it is running through all the possible combinations, so be patient
# Modify the constants to get a different output to the 'word.txt'
from minigames.card_games.word_finder import WordFinder

vowels = "aeiou"
consonants = "bcdfghjklmnpqrstvwxyz"
word_finder  = WordFinder()
max_vowels = 3 # The max amount of vowels in each set of letters; amount of vowels is from (1 -> max_vowels)
total_letters = 6
needed_possible_words = 3 # The amount of words that the letters must be able to produce (can be higher, but not lower)

get_letter_combinations("abc", 3)
all_vowels = get_all_letter_combinations(vowels, max_vowels)
letter_combinations = []
start = time.time()

needed_consonants = -1
all_consonants = 0
for vowels in all_vowels:
    if total_letters - len(vowels) != needed_consonants:
        needed_consonants = total_letters - len(vowels)
        all_consonants = get_letter_combinations(consonants, needed_consonants)
        print("REPLINISH", len(all_consonants), time.time() - start)

    for consonants in all_consonants:
        letter_combinations.append(vowels + consonants)

print("DONE FINDING ALL COMBINATIONS", len(letter_combinations), time.time() - start)

good_letter_combinations = [] # Combinations that can yield more words or the same amount of words as needed_possible_words
for letter_combination in letter_combinations:
    if len(word_finder.get_all_words_of_length(letter_combination, total_letters)) >= needed_possible_words:

        good_letter_combinations.append(list_to_string(letter_combination).upper())
print("DONE FINDING GOOD COMBINATIONS", time.time() - start)

file = open("words.txt", "w+")
file.write(str(good_letter_combinations))

