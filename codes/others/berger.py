from math import log, ceil

def assert_code(data, answ):

	w = data.count('1')
	k = len(data)
	r = ceil(log(k, 2))
	inv = bin(2**r-1)
	check = str(bin(int(bin(w),2) ^ int(inv,2)))
	check = '0'*(r-len(check)+2) + check[2:]

	if data + check == answ :
		return True
	else :
		return False
