import random


def huffman(p):
    if len(p) == 2:
        return dict(zip(sorted(p, key=p.get), ['0', '1']))

    p_prime = p.copy()
    a1, a2 = lowest_prob_pair(p)
    p1, p2 = p_prime.pop(a1), p_prime.pop(a2)
    p_prime[a1 + a2] = p1 + p2

    c = huffman(p_prime)
    ca1a2 = c.pop(a1 + a2)
    c[a1], c[a2] = ca1a2 + '0', ca1a2 + '1'

    return c


def lowest_prob_pair(p):
    assert (len(p) >= 2)

    sorted_p = sorted(p, key=p.get)
    for i in range(len(p) - 1):
        if p[sorted_p[i]] == p[sorted_p[i + 1]] and sorted_p[i] > sorted_p[i + 1]:
            tmp = sorted_p[i]
            sorted_p[i] = sorted_p[i + 1]
            sorted_p[i + 1] = tmp
    return sorted_p[0], sorted_p[1]


def assert_code(data, ans):
    codes = huffman(data)
    if codes == ans:
        return True
    else:
        return False


def generate_for_encode():
    data = {'a' + str(i + 1): 0 for i in range(random.randint(6, 9))}
    some = 100
    for i in range(len(data) - 1):
        if some > 40:
            rand = random.randint(1, 40)
        else:
            rand = random.randint(1, some // 2)
        data['a' + str(i + 1)] = rand / 100
        some -= rand
    data['a' + str(len(data))] = some / 100
    return {'message': data}


def get_details():
    return {
        'view_type': 'huffman',
        'only_encode': True
    }

# tests

# data = { 'a1': 0.25, 'a2': 0.25, 'a3': 0.2, 'a4': 0.15, 'a5': 0.15 }
# ans = {'a4': '110', 'a5': '111', 'a1': '01', 'a2': '10', 'a3': '00'}
# print(huffman(data))
# print(assert_code(data, ans))
# data = generate_for_encode()
# print(data)
