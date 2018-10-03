def assert_code(data,answ):

    data=int(data, 2)
    answ=int(answ, 2)

    if (data ^ (data >> 1)) == answ:
        print("ok!")
        return True
    else:
        print()
        return False


def assert_decode(data,answ):

    data=int(data, 2)
    answ=int(answ, 2)

    sum=data

    while data > 0:
        data = data >> 1
        sum ^= data

    if answ==sum:
        return True
    else:
        return False


