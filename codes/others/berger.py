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


def assert_code(data, answ):

	if data + berger(data) == answ:
		return True
	else :
		return False


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


# def generate_for_decode():


print(assert_code('1001', '100101'))
print(assert_decode(['100101', 2], True))
print(generate_for_encode())


def ddc(N, base):

	if base==[8,4,2,1]:

		ddc = int()
		for i in str(N):
			ddc *=16
			ddc +=int(i)

		return str(bin(ddc))[2:]

	else:

		ddc=str()

		for i in str(N):

			four = [0,0,0,0]
			current_number=int(i)

			for j in range(len(base)):
				if current_number>=base[j]:
					current_number-=base[j]
					four[j]=1

			for j in four:
				ddc+=str(j)

		return ddc


print(ddc(851, [7, 4, 2, 1]))
