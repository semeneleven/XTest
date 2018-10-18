# data = str(number) answ = str(number)
import random


def assert_code(data, answ):
    data = int(data, 2)
    answ = int(answ, 2)

    if (data ^ (data >> 1)) == answ:
        print("ok!")
        return True
    else:
        print()
        return False


# data = str(number) answ = str(number)
def assert_decode(data, answ):
    data = int(data, 2)
    answ = int(answ, 2)

    sum = data

    while data > 0:
        data = data >> 1
        sum ^= data

    if answ == sum:
        return True
    else:
        return False


def generate_for_encode():
    return {'message' :''.join([str(random.randint(0, 1)) for i in range(0, random.randint(6, 8))])}


def generate_for_decode():
    data = int(generate_for_encode(), 2)
    return data ^ (data >> 1)
