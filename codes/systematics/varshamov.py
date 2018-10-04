import math
import numpy as np

standard_C = [[0, 0, 1, 1], [0, 1, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 0]]


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


def compose(M1,M2):

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

# data = [messLength,d (minCodeDistance)], answ = [amount_colums_G, amount_err, amount_rows_G, amount_r]
def initializing_step(data, answ):
    if not data[0] == answ[0]:
        return False

    if not data[1] >= 2 * answ[1] + 1:
        return False

    if not 2 ** answ[3] > sum_d_n(data[1], data[0]):
        return False

    if not data[0] - answ[3] == answ[2]:
        return False

    return True


# data = [t,d], answ = [E,C]
def building_G_step(data, answ):
    E = answ[0]

    if not is_E(E):
        return False

    C = answ[1]

    for row in C:
        if not 2 ** len(row) > sum_d_n(data[1], len(row) + len(E[0])):
            return False
        if not row.count(1) >= data[1] - 1:
            return False

    return True


# data =[G,message] answ= code
def code_step(data, answ):
    message = str(data[1])

    encoded = encode(data[0],message)


    if not encoded == answ:
        return False

    return True


# data=[E,C], answ=[C.T,E]
def building_H_step(data, answ):

    if np.array_equal(np.asmatrix(data[1]).transpose(),np.asmatrix(answ[0])):
        return False

    if not is_E(answ[1]):
        return False

    return True


# data = [G,message], answ = [coded]
def correction_step(data,answ):
    message = str(data[1])
    encoded = encode(data[0], message)

    if not encoded == answ:
        return False

    return True

# TODO generators for each step
print(initializing_step([17, 4], [17, 1, 9, 8]))
print(building_G_step([1, 3], [
    [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0],
     [0, 0, 0, 0, 0, 1]],
    [[0, 0, 1, 1], [0, 1, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 0]]
]))
print(code_step([[[1, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
             [0, 0, 0, 1, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
             [0, 0, 0, 0, 0, 1, 1, 1, 0, 0]], '001110'], '0011100101'))

print(building_H_step([gen_E(6), [[0, 0, 1, 1], [0, 1, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 0]]],
                      [[[0, 0, 1, 0, 0, 1], [0, 1, 0, 1, 0, 1], [1, 0, 0, 1, 1, 0], [1, 1, 1, 0, 0, 0]], gen_E(4)]))

print(correction_step([compose(gen_E(6),standard_C), '001110'], '0011100101'))
