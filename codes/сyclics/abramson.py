# TODO improve algorithm for more then one err
import random

polynomials = {
    4: [[1, 0, 0, 1, 1], [1, 1, 0, 0, 1], [1, 1, 1, 1, 1]],
    3: [[1, 1, 0, 1], [1, 0, 1, 1]]
}


def abramson(msg, polynomial):
    polynomial_num = 0
    for i in polynomial:
        polynomial_num = (polynomial_num << 1) + i

    gen_polynomial_num = (polynomial_num << 1) ^ polynomial_num
    gen_polynomial = bin(gen_polynomial_num)[2:]

    msg = msg + '0' * (2 ** (len(polynomial) - 1) - 1 - len(msg))

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

    polynomial_num = 0

    for i in polynomial:
        polynomial_num = (polynomial_num << 1) + i

    gen_polynomial_num = (polynomial_num << 1) ^ polynomial_num
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
        if R.count('1') <= 1:
            if R.count('1') == 0:
                break
            for i in range(len(decoded) - len(R), len(decoded) - 1):
                decoded = decoded[:i] \
                          + str(int(R[i % len(R)]) ^ int(decoded[i])) \
                          + decoded[(i + 1):]

            for i in range(len(decoded) // len(R) - loop_num):
                decoded = decoded[len(decoded) - len(polynomial):] + decoded[:len(decoded) - len(polynomial)]

            break

        elif R.count('1') > 1:
            R = decoded[len(decoded) - len(polynomial):] + decoded[:len(decoded) - len(polynomial)]
            decoded = R
            R = decoded[decoded.find('1'):]
            loop_num += 1

    if not decoded[:len(decoded) - len(polynomial)] == answer:
        return False

    return True


def generate_for_encode():
    h = 4
    polynomial = polynomials[h][random.randint(0, len(polynomials[h])-1)]
    msg = ''.join([str(random.randint(0, 1)) for i in range(0, random.randint(7, 2**h-1 - len(polynomial)))])
    return [msg, polynomial]


def generate_for_decode():
    data = generate_for_encode()
    msg = data[0]
    polynomial = data[1]
    encoded = abramson(msg,polynomial)
    n = random.randint(0, len(encoded) - 1)
    err = encoded[:n] + ('0' if encoded[n] == '1' else '1') + encoded[(n + 1):]

    return [err, polynomial]


print(abramson('0101100111', polynomials[4][0]))
print(assert_code(['0101100111', polynomials[4][0]], '010110011100101'))
print(assert_decode(['010110001100101', polynomials[4][0]], '0101100111'))
print(generate_for_encode())
print(generate_for_decode())
