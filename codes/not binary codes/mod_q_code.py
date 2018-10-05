import random

def mod_q_code(code, q):
    return code + str(get_letter(q - sum(int(i, q) for i in code) % q))

def get_letter(num):
    if num >= 10 :
        string = 'ABCDEF'
        return string[num-10]
    return num

def assert_code(data, ans):
    code = mod_q_code(data[0], data[1])
    if code == ans:
        return True
    return False

def assert_decode(data, ans):
    istrue = data == mod_q_code(data[0][:len(data[0])-1], data[1])
    if ans == istrue:
        return True
    return False

def generate_to_encode():
    q = random.randint(2,16)
    return ''.join(str(get_letter(random.randint(0,q-1))) for i in range(random.randint(8,12))), q

def generate_to_decode():
    data = generate_to_encode()
    w_error = ['',data[1]]
    print(data)
    if random.randint(1,10) > 4 :
        w_error[0] = data[0][:len(data[0])-1] + str(get_letter(random.randint(0, data[1]-1)))
        return w_error
    return data

# tests
print(mod_q_code('A01B6D1139A24', 14))
print(assert_code(['A01B6D1139A24', 14],'A01B6D1139A24D'))
print(assert_decode(['A01B6D1139A24B', 14], False))
print(generate_to_encode())
print(generate_to_decode())
