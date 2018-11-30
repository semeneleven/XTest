from codes.nonbinary.mod_q_code import mod_q_code, get_letter
import random


def iterative(data):
    q = data['q']
    result = []

    for i in range(len(data['matrix'])):
        result.append(mod_q_code(data['matrix'][i], q))

    checks = ''

    for i in range(len(result[0]) - 1):
        code = ''.join(data[i] for data in result)
        code = mod_q_code(code, q)
        checks = checks + code[len(code) - 1]

    result.append(checks)

    return result, q


# data = [[matrix], q], ans = [matrix]
def assert_code(data, ans):
    print(data['matrix'])
    result = []
    for i in range(len(data['matrix'])):
        result.append(data['matrix'][i]+ans[i])
    result.append(ans[len(ans) - 1])
    print(result)

    code = iterative(data)

    if code[0] == ans:
        return True
    return False


# data = [[matrix], q](data_true), ans = [matrix]
def assert_decode(data, ans):
    if data['data_true'] == ans:
        return True
    return False


def generate_for_encode():
    length = 5
    q = random.randint(2, 16)
    data = []
    for i in range(length):
        data.append(''.join(get_letter(random.randint(0, q - 1)) for i in range(length)))
    return {'matrix': data,'q': q}


def generate_for_decode():
    data_true, q = iterative(generate_for_encode())
    data_error = data_true.copy()

    error_count = random.randint(1, 4)
    error_place = [[], []]

    for i in range(error_count):
        string, column = random.randint(0, 4), random.randint(0, 4)
        if string not in error_place[0] and column not in error_place[1]:
            error_place[0].append(string)
            error_place[1].append(column)

    for i in range(len(error_place[0])):
        error = get_letter(random.randint(1, q - 1))
        error_string, error_column = error_place[0][i], error_place[1][i]

        data_error[error_string] = data_true[error_string][:error_column] + error + data_true[error_string][
                                                                                    error_column + 1:]

    return {'data_true': data_true,'q': q,'data_error': data_error}


def get_details():
    return {'view_type': 'standard',
            'exam_tasks': 6}


def get_name():
    return 'Итеративный'
# tests
# x = ['1303',
#      '2021',
#      '0310',
#      '1201']
# data = [x, 4]
# ans = ['13031',
#        '20213',
#        '03100',
#        '12010',
#        '0013']
#
# print(assert_code(data, ans))
#
# data_encode = generate_for_encode()
# for code in data_encode[0]:
#     print(code)
# print()
#
# data_true, _, data_error = generate_for_decode()
# for code in data_true:
#     print(code)
# print()
#
# for code in data_error:
#     print(code)
# print()
