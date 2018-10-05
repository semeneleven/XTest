

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


# tests
print(shannon_fano({'a1':0.15, 'a2':0.25, 'a3':0.1, 'a4':0.13, 'a5':0.25, 'a6':0.12}))
