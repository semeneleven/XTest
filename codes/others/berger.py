import random
from math import log, ceil


def berger(code):
    w = code.count('1')
    k = len(code)
    r = ceil(log(k, 2))
    inv = bin(2 ** r - 1)
    check = str(bin(int(bin(w), 2) ^ int(inv, 2)))
    check = '0' * (r - len(check) + 2) + check[2:]

    return check


# data = message answ = data + r
def assert_code(data, ans):
    if data['message'] + berger(data['message']) == ans:
        return True
    else:
        return False


# data = [code, r] answ = bool(check for error(true if no error))
def assert_decode(data, ans):
    num = data['message']
    r = data['r']
    k = len(num)

    if not (num[(k - r):] == berger(num[:(k - r)])) == (ans[0] == 'true'):
        return True
    else:
        return False


def generate_for_encode():
    data = str()
    for i in range(random.randint(4, 8)):
        data += str(random.randint(0, 1))

    if int(data) == 0:
        n = random.randint(0, 1)
        data = data[:n] + '1' + data[(n + 1):]

    return {'message': data}


def generate_for_decode():
    data = generate_for_encode()['message']
    check = berger(data)
    if random.randint(0, 10) < 7:
        data = generate_for_encode()['message']
    return {'message': data + check,'r': len(check)}


def get_details():
    return {'view_type': 'standard',
            'exam_tasks': 4}


def get_name():
    return 'Бергера'
# tests
# print(assert_code('1001', '100101'))
# print(assert_decode(['100101', 2], True))
# print(generate_for_encode())
# print(generate_for_decode())
