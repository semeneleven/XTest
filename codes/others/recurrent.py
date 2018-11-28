import random


def recurrent(msg, t):
    result = ''
    for i in range(len(msg) - t):
        result += str(int(msg[i]) ^ int(msg[i + t]))

    result = '0' * (len(msg) - len(result)) + result

    return result


# data = [msg,t]
def assert_code(data, answer):
    msg = data['message']
    t = data['step']

    if not recurrent(msg, t) == answer:
        return False

    return True


# data = [check, t, err_msg]
def assert_decode(data, answer):
    if not recurrent(answer, data[1]) == data[0]:
        return False

    return True


def generate_for_encode():
    t = random.randint(1, 3)
    msg = ''.join([str(random.randint(0, 1)) for i in range(0, random.randint(5, 8))])

    return {'message': '1000001', 'step': 3}#{'message': msg, 'step': t}


def generate_for_decode():
    data = generate_for_encode()
    msg = data['message']
    t = data['step']
    check = recurrent(msg, t)
    n = random.randint(0, len(msg) - 1)
    err_msg = msg[:n] + ('0' if msg[n] == '1' else '1') + msg[(n + 1):]

    return [check, t, err_msg]


def get_details():
    return {'view_type': 'standard'}


def get_name():
    return 'Реккурентные'
