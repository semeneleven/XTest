import random

def shannon_fano(data):
    alfabet = sorted(data, key = data.get, reverse = True)
    result = dict.fromkeys(alfabet, '')
    get_codes(alfabet, data, result)
    return result


def get_codes(group, data, result):
    groups = get_groups(group, data)
    for alf in groups[0]:
        result[alf] += '1'
    for alf in groups[1]:
        result[alf] += '0'
    if len(groups[0]) > 1:
        get_codes(groups[0], data, result)
    if len(groups[1]) > 1:
        get_codes(groups[1], data, result)


def get_groups(alfabet, data):
    dif_sum = []
    for i in range(len(alfabet)//2 + 1):
        sum1 = sum(list(map(lambda alf : data[alf], alfabet[:i])))
        sum2 = sum(list(map(lambda alf : data[alf], alfabet[i:])))
        dif_sum.append(abs(sum1-sum2))
    group_line = dif_sum.index(min(dif_sum))
    return alfabet[:group_line], alfabet[group_line:]


def assert_code(data, ans):
    test = shannon_fano(data)
    if test == ans :
        return True
    else :
        return False


def generate_to_encode():
    alfabet = ['a1','a2','a3','a4','a5','a6']
    data = dict.fromkeys(alfabet, 0)
    some = 100
    for i in range(5):
        if some > 40 : rand = random.randint(1,40)
        else : rand = random.randint(1,some)
        data[alfabet[i]] = rand/100
        some -= rand
    data[alfabet[5]] = some/100
    print(sum(list(map(lambda alf : data[alf], alfabet))))
    return data

# tests
print(shannon_fano({'a1':0.15, 'a2':0.25, 'a3':0.1, 'a4':0.13, 'a5':0.25, 'a6':0.12}))
print(assert_code({'a1':0.15, 'a2':0.25, 'a3':0.1, 'a4':0.13, 'a5':0.25, 'a6':0.12}, {'a1':'011','a2':'11','a3':'000','a4':'010','a5':'10','a6':'001'}))
data = generate_to_encode()
print(data)
print(shannon_fano(data))
