import math
import random

def permutation(alphabet, word_len, words = []):
    n = math.factorial(len(alphabet))

    for word in words:
        if words.count(word) > 1 or len(word) != word_len:
            return False, n
        for letter in word:
            if word.count(letter) > 1 or letter not in alphabet:
                return False, n

    return True, n


def accommodation(alphabet, word_len, words = []):
    boolean, n = permutation(alphabet, word_len, words)

    n /= math.factorial(len(alphabet) - word_len)

    return boolean, n


def certain_combination(alphabet, word_len, words = []):
    bool, n = accommodation(alphabet, word_len, words)
    n /= math.factorial(word_len)

    if not bool:
        return False, n

    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            bool = False
            for symbol in words[i]:
                if symbol not in words[j]:
                    bool = True
            if not bool:
                return False, n

    return True, n


def all_combination(alphabet, word_len, words = []):
    n = len(alphabet)**word_len

    for word in words:
        if words.count(word) > 1 or len(word) != word_len:
            return False, n
        for symbol in word:
            if symbol not in alphabet:
                return False, n

    return True, n


def qualitative_change(alphabet, word_len, words = []):
    n = len(alphabet)*((len(alphabet) - 1)**(word_len - 1))

    for word in words:
        if words.count(word) > 1 or len(word) != word_len:
            return False, n
        for i in range(word_len):
            if word[i] not in alphabet:
                return False, n
            if i != word_len - 1 :
                if word[i] == word[i + 1]:
                    return False, n

    return True, n


# data = ['function', 'alphabet', word_len, int(quantity of words)], ans = [word,...]
def assert_code(data, ans):
    if not len(ans) == data[3]:
        return False

    bool, _ = globals()[data[0]](data[1], data[2], ans)

    return bool


# data = ['function', 'alphabet', word_len, ['word']], ans = True or False(is word matches code requirement)
def assert_decode(data, ans):
    bool, _ = globals()[data[0]](data[1], data[2], data[3])

    return bool == ans


def generate_to_encode():
    data = []

    funcs = ['permutation', 'accommodation', 'certain_combination', 'all_combination', 'qualitative_change']
    data.append(funcs[random.randint(0,4)])

    alphabet = 'abcdefgh'
    data.append(alphabet[:random.randint(3,8)])

    if data[0] == 'permutation':
        data.append(len(data[1]))
    else :
        data.append(random.randint(1,len(data[1])))

    _, n = globals()[data[0]](data[1], data[2])
    if n > 5:
        data.append(random.randint(1,5))
    elif n > 1:
        data.append(random.randint(1,n))
    else :
        data.append(1)

    return data


def generate_to_decode():
    data = generate_to_encode()

    word = ''.join(data[1][random.randint(0,len(data[1])-1)] for i in range(random.randint(1,data[2])))

    data[3] = [word]

    return data

# tests
data = ['qualitative_change', 'abcd', 3, 4]
ans = ['abd','cdc','bcd','bdb']
print(assert_decode(['accommodation','abcd',3,['acd']],True))
print(assert_code(data, ans))
print(generate_to_encode())
print(generate_to_decode())
