from codes.nonbinary.mod_q_code import mod_q_code, get_letter
import random

def iterative(data):
    q = data[1]
    result = []

    for i in range(len(data[0])):
        result.append(mod_q_code(data[0][i], q))

    checks = ''

    for i in range(len(result[0])-1):
        code = ''.join(data[i] for data in result)
        code = mod_q_code(code, q)
        checks = checks + code[len(code)-1]

    result.append(checks)

    return result, q


# data = [[matrix], q], ans = [matrix]
def assert_code(data, ans):
    code = iterative(data)
    if code[0] == ans:
        return True
    return False


# data = [[matrix], q](data_true), ans = [matrix]
def assert_decode(data, ans):
    if data[0] == ans:
        return True
    return False


def generate_to_encode():
    length = 5
    q = random.randint(2,16)
    data = []
    for i in range(length):
        data.append(''.join(get_letter(random.randint(0,q-1)) for i in range(length)))
    return data, q


def generate_to_decode():
    data_true, q = iterative(generate_to_encode())
    data_error = data_true.copy()

    error_count = random.randint(1,4)
    error_place = [[],[]]

    for i in range(error_count):
        string, column = random.randint(0,4), random.randint(0,4)
        if string not in error_place[0] and column not in error_place[1]:
            error_place[0].append(string)
            error_place[1].append(column)

    for i in range(len(error_place[0])):
        error = get_letter(random.randint(1,q-1))
        error_string, error_column = error_place[0][i], error_place[1][i]

        data_error[error_string] = data_true[error_string][:error_column] + error + data_true[error_string][error_column+1:]

    return data_true, q, data_error


# tests
x = ['1303',
     '2021',
     '0310',
     '1201']
data = [x, 4]
ans = ['13031',
       '20213',
       '03100',
       '12010',
       '0013']
print(assert_code(data, ans))

data_encode = generate_to_encode()
for code in data_encode[0]:
    print(code)
print()

data_true, _, data_error = generate_to_decode()
for code in data_true:
    print(code)
print()

for code in data_error:
    print(code)
print()
