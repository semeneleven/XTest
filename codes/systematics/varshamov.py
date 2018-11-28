import math
import random

import numpy as np

standard_C = [
    [0, 0, 1, 1],
    [0, 1, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 1, 0],
    [1, 1, 0, 0]
]


def gen_E(n):
    E = list()

    for i in range(n):
        E.append(list())
        for j in range(n):
            if i == j:
                E[i].append(1)
            else:
                E[i].append(0)

    return E


def sum_d_n(d, n):
    summary = 1

    for i in range(d - 2):
        summary += math.factorial(n - 1) / math.factorial(i) / math.factorial(n - 2)

    return summary


def is_E(E):
    for i in range(len(E)):
        # print("(" + str(i) + ")", end=" ")
        for j in range(len(E[i])):
            # print(E[i][j], end=" ")
            if i == j and not E[i][j] == 1:
                return False

            elif not i == j and not E[i][j] == 0:
                return False
        # print("")
    return True


def compose(M1, M2):
    for i in range(len(M1)):
        M1[i].extend(M2[i])

    return M1


def encode(G, message):
    summary = 0
    for i in range(len(message)):
        if message[i] == '1':
            summary ^= int(''.join([str(x) for x in G[i]]), 2)
    sumstr = str(bin(summary))[2:]
    sumstr = '0' * (len(G[1]) - len(sumstr)) + sumstr

    return sumstr


# data = [messLength,d (minCodeDistance)], answer = [amount_colums_G, amount_err, amount_rows_G, amount_r]
def initializing_step(data, answer):
    if not data[0] == answer[0]:
        return False

    if not data[1] >= 2 * answer[1] + 1:
        return False

    if not 2 ** answer[3] > sum_d_n(data[1], data[0]):
        return False

    if not data[0] - answer[3] == answer[2]:
        return False

    return True


# data = [t,d], answer = [E,C]
def building_G_step(data, answer):
    E = answer[0]

    if not is_E(E):
        return False

    C = answer[1]

    for row in C:
        if not 2 ** len(row) > sum_d_n(data[1], len(row) + len(E[0])):
            return False
        if not row.count(1) >= data[1] - 1:
            return False

    return True


# data =[G,message] answer= code
def code_step(data, answer):
    message = str(data[1])

    encoded = encode(data[0], message)

    if not encoded == answer:
        return False

    return True


# data=[E,C], answer=[C.T,E]
def building_H_step(data, answer):
    if np.array_equal(np.asmatrix(data[1]).transpose(), np.asmatrix(answer[0])):
        return False

    if not is_E(answer[1]):
        return False

    return True


# data = [G,message], answer = [coded]
def correction_step(data, answer):
    message = str(data[1])
    encoded = encode(data[0], message)

    if not encoded == answer:
        return False

    return True


def generator_init_step():
    return [random.randint(17, 20), random.randint(3, 5)]


def generator_build_G_step():
    t = random.randint(1, 2)
    return [t, 2 * t + 1 + random.randint(0, 1)]


def generator_code_step():
    G = compose(gen_E(6), standard_C)
    msg = str()
    for i in range(6):
        msg += str(random.randint(0, 1))

    return [G, msg]


def generator_build_H_step():
    return [gen_E(6), standard_C]


def generator_correction_step():
    G = compose(gen_E(6), standard_C)
    msg = str()
    for i in range(6):
        msg += str(random.randint(0, 1))

    encoded = encode(G,msg)
    print(encoded)

    n = random.randint(0, len(encoded)-1)
    encoded = encoded[:n]+('0' if encoded[n] == '1' else '1')+encoded[(n+1):]

    print(encoded)

    return [G, encoded]


def get_details():
    return {
        'view_type': 'entropy',
        'generators': ['generator_init_step', 'generator_build_G_step', 'generator_code_step', 'generator_build_H_step', 'generator_correction_step'],
        'steps': ['initializing_step', 'building_G_step', 'code_step', 'building_H_step', 'correction_step']
    }


def get_name():
    return 'Варшамова'
# print(initializing_step([17, 4], [17, 1, 9, 8]))
# print(building_G_step([1, 3], [
#     [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0],
#      [0, 0, 0, 0, 0, 1]],
#     [[0, 0, 1, 1], [0, 1, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 0]]
# ]))
# print(code_step([[[1, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
#                   [0, 0, 0, 1, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
#                   [0, 0, 0, 0, 0, 1, 1, 1, 0, 0]], '001110'], '0011100101'))
#
# print(building_H_step([gen_E(6), [[0, 0, 1, 1], [0, 1, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 0]]],
#                       [[[0, 0, 1, 0, 0, 1], [0, 1, 0, 1, 0, 1], [1, 0, 0, 1, 1, 0], [1, 1, 1, 0, 0, 0]], gen_E(4)]))
#
# print(correction_step([compose(gen_E(6), standard_C), '001110'], '0011100101'))
#
# print(generator_init_step())
# print(generator_build_G_step())
# print(generator_code_step())
# print(generator_build_H_step())
# print(generator_correction_step())