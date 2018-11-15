import math
import random


def inf_quantity(probs, code):
    inf = 0

    for i in range(0, len(code), 2):
        inf += math.log2(1 / probs[code[i:i+2]])

    return inf


def entropy(probs, max=False):
    entropy = 0.0

    for key in probs:
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
    if ans[0] == entropy(data, max=True) and ans[1] == entropy(data):
        return True
    return False


# data = [[yx1,...], [yx2,...],...], ans = number
def conditional_entropy_step(data, ans):
    if ans == conditional_entropy(data):
        return True
    return False


def get_probs(length):
     probs = {'x' + str(i+1): 0 for i in range(length)}

     total = 100
     for i in range(len(probs)-1):
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

    code = ''.join('x'+str(random.randint(1,4)) for i in range(random.randint(4,6)))

    return {'probs' : probs, 'code' : code}


def generator_entropy_step():
    data = get_probs(4)

    return {'message': data}


def generator_conditional_entropy_step():
    data = [[], [], []]

    for y in range(3):
        yx = get_probs(3)
        for i in range(3):
            data[i].append(yx['x'+str(i+1)])

    return {'message': data}


def get_details():
    return {
        'view_type': 'entropy',
        'generators': ['generator_inf_quantity_step', 'generator_entropy_step', 'generator_conditional_entropy_step'],
        'steps': ['inf_quantity_step', 'entropy_step', 'conditional_entropy_step']
    }

# tests
# print(entropy({'a':0.35,'b':0.15,'d':0.3,'c':0.2}, True))
# print(generator_inf_quantity_step()['message'])
# print(get_probs(4))
# print(generator_conditional_entropy_step())
print(inf_quantity({'x1':0.4,'x2':0.06,'x3':0.07,'x4':0.47}, 'x2x1x3x2'))
