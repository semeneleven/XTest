import random


def assert_code(data, answ):
    for i in range(len(data)):
        sum = 0
        for j in range(len(data[i])):
            sum ^= data[i][j]
        if not sum == answ[0][i]:
            return False

    for i in range(len(data)):
        sum = 0
        for j in range(len(data[i])):
            sum ^= data[j][i]
        if not sum == answ[1][i]:
            return False

    return True


def assert_decode(data, answ):
    for i in range(len(answ)):
        sum = 0
        for j in range(len(answ[i])):
            sum ^= answ[i][j]
        if not sum == data[0][i]:
            return False

    for i in range(len(answ)):
        sum = 0
        for j in range(len(answ[i])):
            sum ^= answ[j][i]
        if not sum == data[1][i]:
            return False

    return True


def generate_for_encode():
    data = list()
    for i in range(5):
        data.append(list())
        for j in range(5):
            data[i].append(random.randint(0, 1))

    return data


def generate_for_decode():
    answ = generate_for_encode()

    data=[[],[]]

    err_x = random.randint(0, 4)
    err_y = random.randint(0, 4)

    for i in range(len(answ)):
        sum = 0
        for j in range(len(answ[i])):
            sum ^= answ[i][j]
        data[0].append(sum)

    for i in range(len(answ)):
        sum = 0
        for j in range(len(answ[i])):
            sum ^= answ[j][i]
        data[1].append(sum)

    answ[err_x][err_y] ^= 1

    return data, answ


print(assert_code([[1, 0, 1, 0, 1], [0, 1, 1, 0, 1], [0, 0, 1, 1, 1], [0, 1, 0, 0, 1], [1, 0, 1, 0, 1]],
                  [[1, 1, 1, 0, 1], [0, 0, 0, 1, 1]]))
print(assert_decode([[0, 0, 1, 0, 0], [0, 0, 0, 0, 1]],
                    [[0, 0, 0, 0, 0], [1, 0, 0, 1, 0], [1, 0, 0, 0, 0], [1, 1, 1, 1, 0], [1, 1, 1, 0, 1]]))
print(generate_for_encode())
print(generate_for_decode())
