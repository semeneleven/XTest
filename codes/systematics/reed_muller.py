import math
import random


def find_pair(row):
    pair = list()
    for i in range(len(row)):
        if not pair:
            if row[i] == 0:
                pair.append(i)
        else:
            if row[i] == 1:
                pair.append(i)
                break

    return pair


def get_combinations(n, k):
    result = []
    for i in range(0, 1 << n):
        current = i ^ (i >> 1)
        if bin(current).count('1') == k:
            pair = []
            for j in range(n):
                if current & (1 << j):
                    pair.append(j + 1)

            result.append(pair)

    return sorted(result, key=lambda item: item[0])


def C(n, m):
    return math.factorial(m) / math.factorial(n) / math.factorial(m - n)


def sum_C(b, m):
    summary = 0

    for i in range(b + 1):
        summary += C(i, m)

    return int(summary)


def generate_matrix(m, b):

    if not m>b:
        raise ValueError

    k = sum_C(b, m)
    matrix = [[1 for i in range(2 ** m)]]

    # TODO for all b
    indexes = []
    for i in range(1, b):
        indexes.extend(get_combinations(m, i + 1))

    tmp_b = 2

    for i in range(1, k):

        row = [0 for x in range(2 ** m)]

        if i <= m:
            for j in range((2 ** (i - 1)), 2 ** m, ((2 ** (i - 1)) * 2)):
                for k in range(j, (j + 2 ** (i - 1)) if (j + 2 ** (i - 1)) <= 2 ** m else 2 ** m):
                    row[k] = 1
        else:
            rows = indexes[i - m - 1]
            for j in range(2 ** m):
                row[j] = matrix[rows[0]][j]
                for k in range(1, tmp_b):
                    row[j] &= matrix[rows[k]][j]

            if i == sum_C(tmp_b, m) - 1:
                tmp_b += 1

        matrix.append(row)

    return matrix


def reed_muller(data, m=0, b=0, msg=''):
    msg = data[2]
    b = data[1]
    m = data[0]

    matrix = generate_matrix(m, b)
    result = []
    for i in range(len(msg)):
        if msg[i] == '1':
            if not result:
                result = matrix[i]

            else:
                for j in range(len(result)):
                    result[j] = matrix[i][j] ^ result[j]

    return "".join([str(x) for x in result])


# data = [m, b, msg]
def assert_code(data, answer):

    if not reed_muller(data) == answer:
        return False

    return True


# data = [m, b, code]
def assert_decode(data, answer):
    matrix = generate_matrix(data[0], data[1])
    code = data[2]
    b = data[1]
    m = data[0]

    indexes = []
    for i in range(b):
        indexes.extend(get_combinations(m, i + 1))

    decoded = []

    for i in range(len(matrix) - 1, 0, -1):
        delta = 0
        k_arr = []
        for j in range(b):
            if j == 0:
                k_arr.extend(find_pair(matrix[indexes[i - 1][j]]))
                delta = k_arr[1] - k_arr[0]
            else:
                first_k = find_pair(matrix[indexes[i - 1][j]])[1]
                second_k = first_k + delta
                k_arr.append(first_k)
                k_arr.append(second_k)

        decoded.insert(0, sum([int(code[k]) for k in k_arr]) % 2)

        if b > 1 and i == C(b, m) - 1:
            b -= 1

    # TODO if added code with errors
    decoded.insert(0, str(code[0]))

    if not "".join([str(x) for x in decoded]) == answer:
        return False

    return True


def generate_for_encode():

    m = random.randint(3,4)
    b = random.randint(2,m-1)
    message = ''.join([str(random.randint(0,1)) for i in range(sum_C(b,m))])
    return [m, b, message]


def generate_for_decode():

    generated = generate_for_encode()
    return [reed_muller(generated) if i == 2 else generated[i] for i in range(len(generated))]

print(assert_code([4, 2, '01101011010'], '0110001111111010'))
print(assert_decode([4, 2, '0110001111111010'], '01101011010'))
print(generate_for_encode())
print(generate_for_decode())