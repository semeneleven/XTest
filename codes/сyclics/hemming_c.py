# TODO ????????????????

polynomials = {
    4: [[1, 0, 0, 1, 1], [1, 1, 0, 0, 1], [1, 1, 1, 1, 1]],
    3: [[1, 1, 0, 1], [1, 0, 1, 1]]
}


def hemming(msg, polynomial):
    polynomial_num = int(''.join([str(x) for x in polynomial]), 2)

    encoded_num = 0
    for i in polynomial:
        encoded_num = (encoded_num << 1) ^ (int(msg, 2) if i else 0)

    encoded = bin(encoded_num)[2:]
    encoded = '0'*(2**(len(polynomial)-1) - len(encoded) -1)+encoded

    return encoded

# data = [msg,poly]
def assert_code(data, answer):
    if not hemming(data[0], data[1]) == answer:
        return False

    return True


# data [err_msg,poly]
def assert_decode(data, answer):
    msg = data[0]
    polynomial = data[1]

    decoded = msg
    R = msg

    for i in range(len(decoded)-len(polynomial)+2):


        while len(R) >= len(polynomial):
            for j in range(len(polynomial)):
                R = R[:(j)] + str(int(R[j]) ^ int(polynomial[j])) + R[(j + 1):]

            R = R[R.find('1'):]
        print(decoded, R)
        decoded = decoded[len(decoded) - 1:] + decoded[:len(decoded) - 1]
        R = decoded[decoded.find('1'):]



    return True


# print(hemming('01011111010010100010101110', [1, 0, 0, 1, 0, 1]))
# print(assert_code(['01011111010010100010101110', [1, 0, 0, 1, 0, 1]], '0101011001011001001111111010110'))
# print(assert_decode(['1001011001011001001111111010110', [1, 0, 0, 1, 0, 1]], '01011111010010100010101110'))
