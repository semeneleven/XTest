import math


def inf_quantity(probs, code):
    inf = 0

    for symbol in code:
        inf += math.log2(1 / probs[symbol])

    return inf


def entropy(probs, max=False):
    entropy = 0

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


def get_details():
    return {
        'view_type': 'entropy',
        'steps': ['inf_quantity', 'entropy', 'conditional_entropy']
    }

# tests
# print(entropy({'a':0.35,'b':0.15,'d':0.3,'c':0.2}, True))
