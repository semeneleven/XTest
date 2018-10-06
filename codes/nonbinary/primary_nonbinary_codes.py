import math

def permutation(alphabet, word_len, words = []):
    n = math.factorial(word_len)
    for word in words:
        for letter in word:
            if word.count(letter) > 1 or len(word) != word_len:
                return False
    return True


def accommodation(alphabet, word_len, words):


def certain_combination(alphabet, word_len, words):


def all_combination(alphabet, word_len, words):


def qualitative_change(alphabet, word_len, words):
