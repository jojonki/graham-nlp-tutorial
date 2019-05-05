import random


# given probabilities
probs = {
    'mom|dag': 5/6,
    'fat|dag': 1/6,

    'mom|son': 5/8,
    'fat|son': 3/8,

    'dag|mom': 2/3,
    'son|mom': 1/3,

    'dag|fat': 2/5,
    'son|fat': 3/5
}


def sampleOne(probs):
    z = sum(probs.values())
    remaining = random.uniform(0, z)
    for k, v in probs.items():
        remaining -= v
        if remaining <= 0:
            return k


def gibbsSampling():
    samples = {
        'mom,dag': 0,
        'mom,son': 0,
        'fat,dag': 0,
        'fat,son': 0,
    }

    # initial values
    A = 'mom'
    B = 'dag'

    # sampling count
    N = 10000

    for _ in range(N):
        # Bを固定でAをサンプル
        _A = sampleOne({k:v for k, v in probs.items() if k.endswith(B)}).split('|')[0]
        # Aを固定でBをサンプル
        _B = sampleOne({k:v for k, v in probs.items() if k.endswith(A)}).split('|')[0]
        samples['{},{}'.format(_A, _B)] += 1

    print('Result:')
    for k, v in samples.items():
        print('P({}) = {:.3f} ({}/{})'.format(k, v/N, v, N))


if __name__ == '__main__':
    gibbsSampling()
