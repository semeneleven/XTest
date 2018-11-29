import random


def hemming_code(message):
    length_r = 0
    if len(message) in range(10, 12):
        length_r = 4
    elif len(message) in range(12, 16):
        length_r = 5

    for i in range(length_r):
        message = message[:2 ** i - 1] + '0' + message[2 ** i - 1:]

    for i in range(length_r):
        r = [
            sum(
                sum([int(message[k]) for k in
                     range(j, (j + 2 ** i) if (j + 2 ** i) <= len(message) else len(message))]) % 2
                for j in range((2 ** i) - 1,
                               len(message),
                               ((2 ** i) * 2))
            ) % 2
        ]

        message = message[:2 ** i - 1] + str(r[0]) + message[2 ** i:]

    return str(message)


def assert_code(data, answer):

    print(data, answer)
    print(hemming_code(data['message']))
    if not hemming_code(data['message']) == str(answer):
        return False
    return True


def assert_decode(data, answer):
    length_r = 0
    if len(data) in range(14, 16):
        length_r = 4
    elif len(data) in range(17, 21):
        length_r = 5

    syndrome = []

    for i in range(length_r):
        r = sum([
            sum([int(data[k]) for k in range(j, (j + 2 ** i) if (j + 2 ** i) <= len(data) else len(data))]) % 2
            for j in range((2 ** i) - 1,
                           len(data),
                           ((2 ** i) * 2))
        ]) % 2

        syndrome.append(r)

    syndrome = list(reversed(syndrome))
    n = int(''.join([str(x) for x in syndrome]), 2) - 1
    corrected = data[:n] + ('0' if data[n] == '1' else '1') + data[(n + 1):]

    if not corrected == answer:
        return False

    return True


def generate_for_encode():
    return {'message': str().join([str(random.randint(0, 1)) for x in range(random.randint(10, 15))])}


def generate_for_decode():
    encoded = hemming_code(generate_for_encode()['message'])
    n = random.randint(0, len(encoded) - 1)
    encoded = encoded[:n] + ('0' if encoded[n] == '1' else '1') + encoded[(n + 1):]
    return encoded


def get_details():
    return {'view_type': 'standard',
            'exam_tasks': 2}


def get_name():
    return 'Хемминга'
#print(assert_code('011001010001', '10011100010100001'))
#print(assert_decode('1010000101101111001', '1011000101101111001'))
