import random

polynomials = {
    1: [1, 0, 0, 1, 1],
    3: [1, 1, 1, 1, 1],
    5: [1, 1, 1]
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


def multiply(a, b):
    result = (a if int(b[len(b) - 1]) else 0)
    for i in range(len(b) - 1):
        result = (a << (i + 1) if int(b[len(b) - i - 2]) else 0) ^ (result)
    return result


def bch(msg, d):
    gen_polynomial_num = int("".join([str(x) for x in polynomials[1]]), 2)
    for i in range(3, d - 1, 2):
        gen_polynomial_num = multiply(gen_polynomial_num, polynomials[i])

    gen_polynomial = bin(gen_polynomial_num)[2:]

    msg += '0' * (15 - len(msg))
    R = msg[msg.find('1'):]

    while len(R) >= len(gen_polynomial):
        for i in range(len(gen_polynomial)):
            R = R[:(i)] + str(int(R[i]) ^ int(gen_polynomial[i])) + R[(i + 1):]

        R = R[R.find('1'):]

    R = '0' * (len(gen_polynomial) - len(R) - 1) + R
    return msg[:len(msg) - len(R)] + R


def assert_decode(data, answer):
    msg = data[0]
    d = data[1]
    gen_polynomial_num = int("".join([str(x) for x in polynomials[1]]), 2)
    for i in range(3, d - 1, 2):
        gen_polynomial_num = multiply(gen_polynomial_num, polynomials[i])

    gen_polynomial = bin(gen_polynomial_num)[2:]

    print(gen_polynomial, d)
    decoded = msg
    R = msg

    for i in range(len(decoded) - len(gen_polynomial) + 2):

        while len(R) >= len(gen_polynomial):
            for j in range(len(gen_polynomial)):
                R = R[:(j)] + str(int(R[j]) ^ int(gen_polynomial[j])) + R[(j + 1):]

            R = R[R.find('1'):]
        R = '0' * (len(gen_polynomial) - len(R) - 1) + R
        print(decoded, R)
        if R.count('1') == 0:
            break
        elif can_correct(R, (d - 1) // 2):
            for j in range(len(decoded) - len(R), len(decoded) - 1):
                print(j)
                decoded = decoded[:j] \
                          + str(int(R[j % (len(decoded) - len(R))]) ^ int(decoded[j])) \
                          + decoded[(j + 1):]

            for j in range(len(decoded) - i):
                decoded = decoded[len(decoded) - 1:] + decoded[:len(decoded) - 1]

            break
        else:
            decoded = decoded[len(decoded) - 1:] + decoded[:len(decoded) - 1]
            R = decoded[decoded.find('1'):]

    decoded = decoded[:len(decoded) - len(gen_polynomial) + 1]

    if not decoded == answer:
        return False

    return True


def assert_code(data, answer):

    if answer == bch(data['message'], int(data['d'])):
        return True

    return False


def generate_for_encode():
    d = [3, 5, 7][random.randint(0, 2)]
    k = {
        3: 11,
        5: 7,
        7: 5,
    }
    msg = "".join([str(random.randint(0, 1)) for x in range(k[d])])

    return {'message': msg, 'k': k[d], 'd': d}


def generate_for_decode():
    data = generate_for_encode()
    msg = data['message']
    k = data['k']
    d = data['d']
    encoded = bch(msg, d);
    err = encoded
    err_count = random.randint(1, 2)
    n = random.randint(0, len(err) - 2)
    for i in range(err_count):
        err = err[:n+i] + ('0' if err[n+i] == '1' else '1') + err[(n+i + 1):]
    if err_count==1:
        err_count = str(err_count) + " ошибку"
    else:
        err_count = str(err_count) + " ошибки"
    return {'message': err, 'err_c': err_count, 'd': d}


def get_details():
    return {'view_type': 'standard',
            'exam_tasks': 2}


def get_name():
    return 'БЧХ'

#print(bch('11010', 7))
# print(assert_decode(['111011001000111', 7],'10101'))
# print({'message':'00010', 'd':7})