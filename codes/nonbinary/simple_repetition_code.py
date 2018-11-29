import random


def simple_rep_code(code):
    return code * 2


def assert_code(data, ans):
    code = simple_rep_code(data['message'])
    if code == ans:
        return True
    return False


def assert_decode(data, ans):
    code = data['message'][:len(data['message']) // 2]
    if code == ans:
        return True
    return False


def generate_for_encode():
    return {'message': ''.join(str(random.randint(0, 9)) for i in range(random.randint(5, 10)))}


def generate_for_decode():
    return {'message' : generate_for_encode()['message'] * 2}


def get_details():
    return {'view_type': 'standard'}


def get_name():
    return 'Простого повторения'
# tests
# print(simple_rep_code('1001'))
# print(assert_encode('297639', '297639297639'))
# print(assert_decode('192874192874', '192874'))
# print(generate_for_encode())
# print(generate_for_decode())
