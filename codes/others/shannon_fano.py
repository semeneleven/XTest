import random

def shannon_fano(data):
    alphabet = sorted(data, key = data.get, reverse = True)
    for i in range(len(data)-1):
        if data[alphabet[i]] == data[alphabet[i+1]] and alphabet[i] < alphabet[i+1] :
            tmp = alphabet[i]
            alphabet[i] = alphabet[i+1]
            alphabet[i+1] = tmp
    result = dict.fromkeys(alphabet, '')
    get_codes(alphabet, data, result)
    return result


def get_codes(group, data, result):
    groups = get_groups(group, data)
    for alph in groups[0]:
        result[alph] += '1'
    for alph in groups[1]:
        result[alph] += '0'
    if len(groups[0]) > 1:
        get_codes(groups[0], data, result)
    if len(groups[1]) > 1:
        get_codes(groups[1], data, result)


def get_groups(alphabet, data):
    dif_sum = []
    for i in range(len(alphabet)//2):
        sum1 = sum(list(map(lambda alph : data[alph], alphabet[:i+1])))
        sum2 = sum(list(map(lambda alph : data[alph], alphabet[i+1:])))
        dif_sum.append(abs(sum1-sum2))
    group_line = dif_sum.index(min(dif_sum)) + 1
    return alphabet[:group_line], alphabet[group_line:]


def assert_code(data, ans):
    codes = shannon_fano(data)
    if codes == ans :
        return True
    else :
        return False


def generate_for_encode():
    data = { 'a' + str(i+1) : 0 for i in range(random.randint(6,9)) }
    some = 100
    for i in range(len(data)-1):
        if some > 40 : rand = random.randint(1,40)
        else : rand = random.randint(1,some//2)
        data['a' + str(i+1)] = rand/100
        some -= rand
    data['a' + str(len(data))] = some/100
    return {'message': data}


def get_details():
    return {
        'view_type': 'standard',
        'only_encode': True
    }


def get_name():
    return 'Шенона-Фано'
# tests print(shannon_fano({'a1':0.15, 'a2':0.24, 'a3':0.1, 'a4':0.13, 'a5':0.26, 'a6':0.12})) print(assert_code({
# 'a1':0.15, 'a2':0.25, 'a3':0.1, 'a4':0.13, 'a5':0.25, 'a6':0.12}, {'a1':'011','a2':'10','a3':'000','a4':'010',
# 'a5':'11','a6':'001'})) data = generate_for_encode() print(data) print(shannon_fano(data))
