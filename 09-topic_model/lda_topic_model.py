import math
import random
from tqdm import tqdm


K = 2
alpha = 0.1
beta = 0.001
xcorpus, ycorpus = [], []
xcounts, ycounts = {}, {}


def sampleOne(probs):
    z = sum(probs)
    remaining = random.uniform(0, z)
    for k, v in enumerate(probs):
        remaining -= v
        if remaining <= 0:
            return k

    return len(probs) - 1


def mapAddCounts(map_data, key, add_count):
    if key not in map_data:
        map_data[key] = 0
    map_data[key] += add_count


def addCounts(word, topic, doc_id, add_count):
    mapAddCounts(xcounts, topic, add_count)
    mapAddCounts(xcounts, '{}|{}'.format(word, topic), add_count)
    mapAddCounts(ycounts, doc_id, add_count)
    mapAddCounts(ycounts, '{}|{}'.format(topic, doc_id), add_count)


def main(in_f):
    # Initialize
    vocabs = []
    n_docs = 0
    with open(in_f, 'r') as fin:
        lines = fin.readlines()
        n_docs = len(lines)
        for doc_id, line in enumerate(lines):
            topics = []
            words = line.strip().split(' ')
            vocabs += words
            for word in words:
                topic = random.randint(0, K-1)
                topics.append(topic)
                addCounts(word, topic, doc_id, 1)

            xcorpus.append(words)
            ycorpus.append(topics)
    vocabs = set(vocabs)
    # initialize all possible elms of xcounts and ycounts
    for k in range(K):
        for word in vocabs:
            if k not in xcounts:
                xcounts[k] = 0
            if '{}|{}'.format(word, k) not in xcounts:
                xcounts['{}|{}'.format(word, k)] = 0
        for doc_id in range(n_docs):
            if doc_id not in ycounts:
                ycounts[doc_id] = 0
            if '{}|{}'.format(k, doc_id) not in ycounts:
                ycounts['{}|{}'.format(k, doc_id)] = 0

    # Samples
    N = 1000
    for _ in tqdm(range(N)):
        ll = 0
        for i, words in enumerate(xcorpus): # i: doc_id
            for j, x in enumerate(words): # j: word_pos
                y = ycorpus[i][j]
                addCounts(x, y, i, -1)
                probs = []
                for k in range(K):
                    # P(x|k): トピックkで単語xの確率
                    num = xcounts['{}|{}'.format(x, k)] + beta
                    den =  xcounts[k] + beta * len(vocabs)
                    p_x_k = num / den

                    # P(k|Y): 文書Y_iでトピックkの確率
                    num = ycounts['{}|{}'.format(k, i)] + alpha
                    den = ycounts[i] +alpha * K
                    p_k_Y =  num / den

                    # その単語xの生起確率を計算する
                    prob = p_x_k * p_k_Y # P(x|k) * P(k|Y): 単語確率 x トピック確率
                    probs.append(prob)

                # 単語xに対して新しくサンプルしたトピックnew_yを割り当てる
                new_y = sampleOne(probs)
                ll -= math.log(probs[new_y])
                addCounts(x, new_y, i, 1)
                ycorpus[i][j] = new_y
                # print('ll:', ll)

    for i, words in enumerate(xcorpus): # i: doc_id
        for j, x in enumerate(words): # j: word_pos
            y = ycorpus[i][j]
            print('{}({}) '.format(x, y), end='')
        print()


if __name__ == '__main__':
    # in_f = './data/wiki-en-documents.word'
    in_f = './data/07-train.txt'
    main(in_f)
