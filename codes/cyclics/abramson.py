# TODO improve algorithm for more then one err
import random

polynomials = {
    4: [[1, 0, 0, 1, 1], [1, 1, 0, 0, 1], [1, 1, 1, 1, 1]],
    3: [[1, 1, 0, 1], [1, 0, 1, 1]]
}


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


def abramson(msg, polynomial):
    polynomial_num = int(''.join([str(x) for x in polynomial]), 2)

    gen_polynomial_num = 0
    C_polynomial_num = 3

    for i in bin(C_polynomial_num)[2:]:
        gen_polynomial_num = (gen_polynomial_num << 1) ^ (polynomial_num if int(i) else 0)

    gen_polynomial = bin(gen_polynomial_num)[2:]

    msg = msg + '0' * len(polynomial)
    R = msg[msg.find('1'):]

    while len(R) > len(polynomial):
        for i in range(len(gen_polynomial)):
            R = R[:(i)] + str(int(R[i]) ^ int(gen_polynomial[i])) + R[(i + 1):]

        R = R[R.find('1'):]

    R = '0' * (len(polynomial) - len(R)) + R

    return msg[:len(msg) - len(R)] + R


# data = [msg,poly]
def assert_code(data, answer):
    if not abramson(data[0], data[1]) == answer:
        return False

    return True


# data [err_msg,poly]
def assert_decode(data, answer):
    msg = data[0]
    polynomial = data[1]

    polynomial_num = int(''.join([str(x) for x in polynomial]), 2)

    gen_polynomial_num = 0

    C_polynomial_num = 3

    for i in bin(C_polynomial_num)[2:]:
        gen_polynomial_num = (gen_polynomial_num << 1) ^ (polynomial_num if int(i) else 0)

    gen_polynomial = bin(gen_polynomial_num)[2:]

    R = msg[msg.find('1'):]
    decoded = msg
    loop_num = 0
    while True:

        while len(R) > len(polynomial):
            for i in range(len(gen_polynomial)):
                R = R[:(i)] + str(int(R[i]) ^ int(gen_polynomial[i])) + R[(i + 1):]

            R = R[R.find('1'):]

        R = '0' * (len(polynomial) - len(R)) + R
        if R.count('1') == 0:
            break
        elif can_correct(R, 2):

            for i in range(len(decoded) - len(R), len(decoded) - 1):
                decoded = decoded[:i] \
                          + str(int(R[i % len(R)]) ^ int(decoded[i])) \
                          + decoded[(i + 1):]

            for i in range(len(decoded)  - loop_num):
                decoded = decoded[len(decoded) - 1:] + decoded[:len(decoded) - 1]

            break

        else:
            R = decoded[len(decoded) - 1:] + decoded[:len(decoded) - 1]
            decoded = R
            R = decoded[decoded.find('1'):]
            loop_num += 1

    if not decoded[:len(decoded) - len(polynomial)] == answer:
        return False

    return True


def generate_for_encode():
    h = 4
    polynomial = polynomials[h][random.randint(0, len(polynomials[h]) - 1)]
    msg = ''.join([str(random.randint(0, 1)) for i in range(0, random.randint(7, 2 ** h - 1 - len(polynomial)))])
    return {'message': msg, 'poly': polynomial}


def generate_for_decode():
    data = generate_for_encode()['message']
    msg = data['message']
    polynomial = data['poly']
    encoded = abramson(msg, polynomial)
    err = encoded
    for i in range(random.randint(1, 2)):
        n = random.randint(0, len(err) - 1)
        err = err[:n] + ('0' if err[n] == '1' else '1') + err[(n + 1):]

    return [err, polynomial]


def get_details():
    return {'view_type': 'standard'}


# print(abramson('00111110', [1, 0, 0, 1, 1]))
# print(assert_code(['00111110', [1, 0, 0, 1, 1]], '0011111011100'))
# print(assert_decode(['010110001100101', polynomials[4][0]], '0101100111'))
# print(generate_for_encode())
# print(generate_for_decode())
