import random


def mod_q_code(code, q):
    b = get_letter(q - sum(int(i, q) for i in code) % q)
    if b == get_letter(q):
        b = '0'
    return code + b


def get_letter(num):
    if num >= 10 and num < 16:
        string = 'ABCDEF'
        return string[num - 10]
    return str(num)


def assert_code(data, ans):
    code = mod_q_code(data[0], data[1])
    if code == ans:
        return True
    return False


def assert_decode(data, ans):
    istrue = data == mod_q_code(data[0][:len(data[0]) - 1], data[1])
    if ans == istrue:
        return True
    return False


def generate_for_encode(q=random.randint(2, 16), length=random.randint(8, 12)):
    return {'message': [''.join(get_letter(random.randint(0, q - 1)) for i in range(length)), q]}


def generate_for_decode():
    data = generate_for_encode()['message']
    w_error = ['', data[1]]
    print(data)
    if random.randint(1, 10) > 4:
        w_error[0] = data[0][:len(data[0]) - 1] + get_letter(random.randint(0, data[1] - 1))
        return w_error
    return data


def get_details():
    return {'view_type': 'standard'}

# tests
# print(mod_q_code('A01B6D1139A24', 16))
# print(assert_code(['A01B6D1139A24', 14],'A01B6D1139A24D'))
# print(assert_decode(['A01B6D1139A24B', 14], False))
# print(generate_for_encode(8))
# print(generate_for_decode())
