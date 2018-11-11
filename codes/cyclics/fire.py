import random

polynomials = {2: [1, 1, 1]}


def gdc(a, b):
    return gdc(b, a % b) if b else a


def lcm(a, b):
    return a * b // gdc(a, b)


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


def fire(msg, polynomial, err_f, err_c):
    L = err_c
    C = err_f + err_c - 1

    while L != 1 and C % (2 ** L - 1) == 0:
        C += 1

    if len(polynomial) - 1 != L:
        raise ValueError("Invalid polynomial")

    C_polynomial_num = 2 ** C + 1

    polynomial_num = int(''.join([str(x) for x in polynomial]), 2)

    gen_polynomial_num = 0

    for i in bin(C_polynomial_num)[2:]:
        gen_polynomial_num = (gen_polynomial_num << 1) ^ (polynomial_num if int(i) else 0)

    gen_polynomial = bin(gen_polynomial_num)[2:]

    msg = msg + '0' * (lcm(2 ** L - 1, C) - len(msg))
    R = msg[msg.find('1'):]

    while len(R) >= len(gen_polynomial):
        for i in range(len(gen_polynomial)):
            R = R[:(i)] + str(int(R[i]) ^ int(gen_polynomial[i])) + R[(i + 1):]

        R = R[R.find('1'):]

    R = '0' * (len(polynomial) - len(R)) + R

    return msg[:len(msg) - len(R)] + R


# data = [msg,poly,err_f,err_c]
def assert_code(data, answer):
    if not fire(data[0], data[1], data[2], data[3]) == answer:
        return False

    return True


# data [err_msg,poly,err_count]
def assert_decode(data, answer):
    msg = data[0]
    polynomial = data[1]
    L = data[2]

    if L > len(polynomial) - 1:
        raise ValueError("Too many errors({})! Can correct only {}!".format(L, len(polynomial) - 1))

    C = 2 * L - 1
    while L != 1 and C % (2 ** L - 1) == 0:
        C += 1

    polynomial_num = int(''.join([str(x) for x in polynomial]), 2)
    gen_polynomial_num = 0

    C_polynomial_num = 2 ** C + 1

    for i in bin(C_polynomial_num)[2:]:
        gen_polynomial_num = (gen_polynomial_num << 1) ^ (polynomial_num if int(i) else 0)

    gen_polynomial = bin(gen_polynomial_num)[2:]

    R = msg[msg.find('1'):]
    decoded = msg
    loop_num = 0
    while True:

        while len(R) >= len(gen_polynomial):
            for i in range(len(gen_polynomial)):
                R = R[:(i)] + str(int(R[i]) ^ int(gen_polynomial[i])) + R[(i + 1):]

            R = R[R.find('1'):]

        R = '0' * (len(gen_polynomial) - len(R) - 1) + R

        if R.count('1') == 0:
            break
        elif can_correct(R, L):

            for i in range(len(decoded) - len(R), len(decoded) - 1):
                decoded = decoded[:i] \
                          + str(int(R[i % len(R)]) ^ int(decoded[i])) \
                          + decoded[(i + 1):]

            for i in range(len(decoded) - loop_num):
                decoded = decoded[len(decoded) - 1:] + decoded[:len(decoded) - 1]

            break

        else:
            R = decoded[len(decoded) - 1:] + decoded[:len(decoded) - 1]
            decoded = R
            R = decoded[decoded.find('1'):]
            loop_num += 1

    if not decoded[:len(decoded) - len(gen_polynomial) + 1] == answer:
        return False

    return True


def generate_for_encode():
    polynomial = polynomials[2]
    msg = ''.join([str(random.randint(0, 1)) for i in range(0, random.randint(4, 6))])
    return {'message': [msg, polynomial, 2, 2]}


def generate_for_decode():
    data = generate_for_encode()['message']
    msg = data[0]
    polynomial = data[1]
    encoded = fire(msg, polynomial, 2, 2)
    err = encoded
    for i in range(random.randint(1, 2)):
        n = random.randint(0, len(err) - 1)
        err = err[:n] + ('0' if err[n] == '1' else '1') + err[(n + 1):]

    return [err, polynomial, 2]

def get_details():
    return {'view_type': 'standard'}

# print(fire('110110', [1, 1, 1], 2, 2))
# print(assert_code(['110110', [1, 1, 1], 2, 2], '110110110110'))
# print(assert_decode(['110110011101', [1, 1, 1], 2], '110000'))
# print(generate_for_encode())
# print(generate_for_decode())
