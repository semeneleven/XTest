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
    if not m > b:
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


def reed_muller(data, msg='', b=0, m=0):
    msg = data['message'] if msg == '' else msg
    b = int(data['b']) if b == 0 else b
    m = int(data['m']) if m == 0 else m

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
    # matrix = generate_matrix(data[0], data[1])
    # code = data[2]
    # b = data[1]
    # m = data[0]
    #
    # indexes = []
    # for i in range(b):
    #     indexes.extend(get_combinations(m, i + 1))
    #
    # decoded = []
    #
    # for i in range(len(matrix) - 1, 0, -1):
    #     delta = 0
    #     k_arr = []
    #     for j in range(b):
    #         if j == 0:
    #             k_arr.extend(find_pair(matrix[indexes[i - 1][j]]))
    #             delta = k_arr[1] - k_arr[0]
    #         else:
    #             first_k = find_pair(matrix[indexes[i - 1][j]])[1]
    #             second_k = first_k + delta
    #             k_arr.append(first_k)
    #             k_arr.append(second_k)
    #
    #     decoded.insert(0, sum([int(code[k]) for k in k_arr]) % 2)
    #
    #     if b > 1 and i == C(b, m) - 1:
    #         b -= 1
    #
    # # TODO if added code with errors
    # decoded.insert(0, str(code[0]))
    #
    # if not "".join([str(x) for x in decoded]) == answer:
    #     return False
    #
    # return True
    if not reed_muller(data, msg=answer) == data['coded']:
        return False

    return True


def generate_for_encode():
    m = random.randint(3, 4)
    b = random.randint(2, m - 1)
    if m==4 and b == 3:
        b-=1
    message = ''.join([str(random.randint(0, 1)) for i in range(sum_C(b, m))])
    return {'message': message, 'm': m, 'b': b, 'matrix': generate_matrix(m, b),
            'zeros': [0 for i in range(2**m)],'k': sum_C(b, m), 'cols': (2**m)*1.4, 'c':2**m}


def generate_for_decode():
    data = generate_for_encode()
    data['coded'] = reed_muller(data)
    data['zeros'] = [0 for i in range(sum_C(data['b'], data['m']))]
    return data


def get_details():
    return {'view_type': 'standard',
            'exam_tasks': 2}


def get_name():
    return 'Рида-Маллера'
# print(assert_code([4, 2, '01101011010'], '0110001111111010'))
# print(assert_decode([4, 2, '0110001111111010'], '01101011010'))
# print(generate_for_encode())
# print(generate_for_decode())
