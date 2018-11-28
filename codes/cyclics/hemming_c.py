# TODO ????????????????

polynomials = {
    4: [[1, 0, 0, 1, 1], [1, 1, 0, 0, 1], [1, 1, 1, 1, 1]],
    3: [[1, 1, 0, 1], [1, 0, 1, 1]]
}


def multiply(a, b):
    result = (a if int(b[len(b) - 1]) else 0)
    for i in range(len(b) - 1):
        result = (a << (i + 1) if int(b[len(b) - i - 2]) else 0) ^ (result)
    return result


def can_correct(R, max_err):
    start = 0
    no_more = False
    while True:

        i = R.find('1', start)

        if i == -1:
            break
        elif no_more:
            return False
        else:
            start = i + 1

        count = 0
        for j in range(i, len(R)):
            if R[j] == '0':
                if count >= 1:
                    no_more = True
                start = j
                break

            count += 1

            if count > max_err:
                return False
    return True


def hemming(msg, polynomial):
    encoded_num = multiply(int(msg, 2), polynomial)

    encoded = bin(encoded_num)[2:]
    encoded = '0' * (2 ** (len(polynomial) - 1) - len(encoded) - 1) + encoded

    return encoded


# data = [msg,poly]
def assert_code(data, answer):
    if not hemming(data[0], data[1]) == answer:
        return False

    return True


# data [err_msg,poly]
def assert_decode(data, answer):
    msg = data[0]
    polynomial = data[1]

    decoded = msg
    R = msg

    for i in range(len(decoded) - len(polynomial) + 2):

        while len(R) >= len(polynomial):
            for j in range(len(polynomial)):
                R = R[:(j)] + str(int(R[j]) ^ int(polynomial[j])) + R[(j + 1):]

            R = R[R.find('1'):]
        R = '0' * (len(polynomial) - len(R) - 1) + R

        if R.count('1') == 0:
            break
        elif can_correct(R, 1):
            for j in range(len(decoded) - len(R), len(decoded) - 1):
                decoded = decoded[:j] \
                          + str(int(R[j % (len(decoded) - len(R))]) ^ int(decoded[j])) \
                          + decoded[(j + 1):]

            for j in range(len(decoded) - i):
                decoded = decoded[len(decoded) - 1:] + decoded[:len(decoded) - 1]

            break
        else:
            decoded = decoded[len(decoded) - 1:] + decoded[:len(decoded) - 1]
            R = decoded[decoded.find('1'):]

    polynomial_num = int(''.join([str(x) for x in polynomial]), 2)

    result = ''

    while True:

        polynomial_num_tmp = polynomial_num << (len(decoded) - len(polynomial) - decoded.find('1'))
        result += '0' * decoded.find('1')
        decoded = decoded[decoded.find('1'):]

        if len(decoded) < len(polynomial):
            break

        polynomial_tmp = bin(polynomial_num_tmp)[2:]

        for i in range(len(decoded)):
            decoded = decoded[:i] + str(int(decoded[i]) ^ int(polynomial_tmp[i])) + decoded[i + 1:]
        decoded = decoded[1:]
        result += '1'

    result += '0' * ((len(msg) - len(polynomial) + 1) - len(result))

    if not result == answer:
        return False

    return True


# TODO generators
def get_details():
    return {'view_type': 'standard'}


def get_name():
    return 'Хемминга'
# print(hemming('01011111010', [1, 1, 0, 0, 1]))
# print(assert_code(['01011111010', [1, 1, 0, 0, 1]], '011101010001010'))
# print(assert_decode(['011101010001010', [1, 1, 0, 0, 1]], '01011111010'))
