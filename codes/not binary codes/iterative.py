from mod_q_code import mod_q_code

def iterative(data):
    q = data[1]

    for i in range(len(data[0])):
        data[0][i] = mod_q_code(data[0][i], q)

    checks = ''

    for i in range(len(data[0][0])-1):
        code = ''.join(data[i] for data in data[0])
        code = mod_q_code(code, q)
        checks = checks + code[len(code)-1]

    data[0].append(checks)

    return data

# tests
x = ['1303',
     '2021',
     '0310',
     '1201']
data = [x, 4]
data = iterative(data)
for code in data[0]:
    print(code)
