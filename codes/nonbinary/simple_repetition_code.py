import random

def simple_rep_code(code):
    return code * 2

def assert_encode(data, ans):
    code = simple_rep_code(data)
    if code == ans:
        return True
    return False

def assert_decode(data, ans):
    code = data[:len(data)//2]
    if code == ans :
        return True
    return False

def generate_for_encode():
    return ''.join(str(random.randint(0,9)) for i in range(random.randint(5,10)))

def generate_for_decode():
    return generate_for_encode() * 2


# tests
print(simple_rep_code('1001'))
print(assert_encode('297639', '297639297639'))
print(assert_decode('192874192874', '192874'))
print(generate_for_encode())
print(generate_for_decode())
