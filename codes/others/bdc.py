import random

bases = [
    [8, 4, 2, 1],
    [7, 4, 2, 1],
    [5, 4, 2, 1],
    [2, 4, 2, 1]]


def bdc(N, base):

    bdc = str()

    for i in str(N):
        four = [0, 0, 0, 0]
        current_number = int(i)

        for j in range(len(base)):
            if current_number >= base[j]:
                current_number -= base[j]
                four[j] = 1

        for j in four:
            bdc += str(j)

    return bdc


def bdc_decode(code, base):
    result = 0
    for i in range(len(code) // 4):
        four = code[i * 4:i * 4 + 4]
        num = 0
        for j in range(len(four)):
            num += int(four[j]) * base[j]
        result = result * 10 + num
    return result


# data = [number, base] answ = str(code)
def assert_code(data, answ):
    print(answ)
    print(bdc_decode(answ, data['base']))
    if bdc_decode(answ, data['base']) == data['message']:
        return True
    else:
        return False


# data = [code, base] answ = number
def assert_decode(data, ans):
    print(bdc_decode(data['message'], data['base']))
    if bdc_decode(data['message'], data['base']) == int(ans):
        return True
    else:
        return False


def generate_for_encode():
    return {'message': random.randint(101, 999),'base': bases[random.randint(0, 3)]}


def generate_for_decode():
    data = generate_for_encode()
    base = bases[random.randint(0, 3)]

    return {'message': bdc(data['message'], base),'base': base}


def get_details():
    return {'view_type': 'standard',
            'exam_tasks': 6}


def get_name():
    return 'ДДК'
# tests
# print(bdc(851, [7, 4, 2, 1]))
# print(assert_code([851, [5, 4, 2, 1]], '101110000001'))
# print(assert_decode(['100101010001', [7, 4, 2, 1]], 851))
# print(generate_for_encode())
# print(generate_for_decode())
