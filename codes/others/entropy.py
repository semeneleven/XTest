import math
import random


def inf_quantity(probs, code):
    inf = 0

    for i in range(0, len(code), 2):
        inf += math.log2(1 / probs[code[i:i + 2]])

    return inf


def entropy(probs, max=False):
    entropy = float(0)

    for key in probs:
        print(probs[key])
        entropy -= probs[key] * math.log2(probs[key])

    if max:
        entropy = math.log2(len(probs))

    return entropy


def conditional_entropy(cond_probs):
    entropy = 0

    for x in cond_probs:
        for yx in x:
            entropy -= yx * math.log2(yx)

    return entropy


# data = [{probs}, str(code)], ans = number
def inf_quantity_step(data, ans):
    if float(ans) == round(inf_quantity(data['probs'], data['code']), 3):
        return True
    return False


# data = {probs}, ans = [max_entropy, entropy]
def entropy_step(data, ans):
    if float(ans[0]) == round(entropy(data['message'], max=True), 3) and float(ans[1]) == round(
            entropy(data['message']), 3):
        return True
    return False


# data = [[yx1,...], [yx2,...],...], ans = number
def conditional_entropy_step(data, ans):
    cond_probs = []

    for i in range(3):
        cond_probs.append(data['message']['x' + str(i + 1)].copy())

    if float(ans) == round(conditional_entropy(cond_probs), 3):
        return True
    return False


def get_probs(length):
    probs = {'x' + str(i + 1): 0 for i in range(length)}

    total = 100
    for i in range(len(probs) - 1):
        if total > 40:
            rand = random.randint(1, 40)
        else:
            rand = random.randint(1, total // 2)
        probs['x' + str(i + 1)] = rand / 100
        total -= rand
    probs['x' + str(len(probs))] = total / 100

    return probs


def generator_inf_quantity_step():
    probs = get_probs(4)

    code = ''.join('x' + str(random.randint(1, 4)) for i in range(random.randint(4, 6)))

    return {'probs': probs, 'code': code}
    # return {'probs': {'x1':0.28,'x2':0.04,'x3':0.19,'x4':0.49}, 'code':'x2x2x4x1x3'} #14.549


def generator_entropy_step():
    data = get_probs(4)

    return {'message': data}
    # return {'message':{'x1':0.28,'x2':0.01,'x3':0.26,'x4':0.45}} # 2.0 1.604


def generator_conditional_entropy_step():
    data = {'x1': [], 'x2': [], 'x3': []}

    for y in range(3):
        yx = get_probs(3)
        for i in range(3):
            data['x' + str(i + 1)].append(yx['x' + str(i + 1)])

    return {'message': data}
    # return {'message': {'x1':[0.2,0.17,0.01], 'x2':[0.32,0.09,0.39], 'x3':[0.48,0.74,0.6]}} #3.606


def get_details():
    return {
        'view_type': 'entropy',
        'generators': ['generator_inf_quantity_step', 'generator_entropy_step', 'generator_conditional_entropy_step'],
        'steps': ['inf_quantity_step', 'entropy_step', 'conditional_entropy_step'],
        'only_encode': True
    }


def get_name():
    return 'Энтропия'
# tests
# print(entropy({'a':0.35,'b':0.15,'d':0.3,'c':0.2}, True))
# print(generator_inf_quantity_step()['message'])
# print(get_probs(4))
# print(generator_conditional_entropy_step())
# print(inf_quantity({'x1':0.28,'x2':0.04,'x3':0.19,'x4':0.49}, 'x2x2x4x1x3'))
# print(entropy({'x1':0.28,'x2':0.01,'x3':0.26,'x4':0.45}, True))
# print(entropy({'x1':0.28,'x2':0.01,'x3':0.26,'x4':0.45}))
