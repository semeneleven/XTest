import random
from math import log, ceil


def berger(code):
	w = code.count('1')
	k = len(code)
	r = ceil(log(k, 2))
	inv = bin(2 ** r - 1)
	check = str(bin(int(bin(w), 2) ^ int(inv, 2)))
	check = '0' * (r - len(check) + 2) + check[2:]

	return check


# data = message answ = data + r
def assert_code(data, answ):

	if data + berger(data) == answ:
		return True
	else :
		return False


# data = [code, r] answ = bool(check for error(true if no error))
def assert_decode(data, answ):

	num =  data[0]
	r = data[1]
	k = len(num)

	if (num[(k-r):] == berger(num[:(k-r)])) == answ:
		return True
	else :
		return False


def generate_for_encode():
	data = str()
	for i in range(random.randint(4, 8)):
		data += str(random.randint(0, 1))

	if int(data) == 0:
		n=random.randint(0, 1)
		data=data[:n]+'1'+data[(n+1):]

	return data


def generate_for_decode():
	data = generate_for_encode()
	check = berger(data)
	if random.randint(0,10) < 5 :
		data = generate_for_encode()
	return data + check, len(check)


# tests
print(assert_code('1001', '100101'))
print(assert_decode(['100101', 2], True))
print(generate_for_encode())
print(generate_for_decode())

