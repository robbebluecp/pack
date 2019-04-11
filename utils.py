import numpy as np
import jieba
import jieba.analyse
from collections import Counter

def word_2_vec(words1, words2):
    # 词向量
    words1_info = jieba.analyse.extract_tags(words1, withWeight=True)
    words2_info = jieba.analyse.extract_tags(words2, withWeight=True)
    # 转成counter不需要考虑0的情况
    words1_dict = Counter({i[0]: i[1] for i in words1_info})
    words2_dict = Counter({i[0]: i[1] for i in words2_info})
    bags = set(words1_dict.keys()).union(set(words2_dict.keys()))
    # 转成list对debug比较方便吗，防止循环集合每次结果不一致
    bags = sorted(list(bags))
    vec_words1 = [words1_dict[i] for i in bags]
    vec_words2 = [words2_dict[i] for i in bags]
    # 转numpy
    vec_words1 = np.asarray(vec_words1, dtype=np.float)
    vec_words2 = np.asarray(vec_words2, dtype=np.float)
    return vec_words1, vec_words2


def cosine_similarity(v1, v2):
    # 余弦相似度
    v1, v2 = np.asarray(v1, dtype=np.float), np.asarray(v2, dtype=np.float)
    up = np.dot(v1, v2)
    down = np.linalg.norm(v1) * np.linalg.norm(v2)
    return round(up / down, 3)


def euclid_distince(v1, v2):
    # 欧氏距离
    v1 /= np.sum(v1)
    v2 /= np.sum(v2)
    v1, v2 = np.asarray(v1, dtype=np.float), np.asarray(v2, dtype=np.float)
    return round(np.linalg.norm(v1 - v2), 3)

def softmax(x_input):
    x_input = np.asarray(x_input, dtype=np.float) / max(x_input)
    return np.exp(x_input) / np.sum(np.exp(x_input))


def sigmoid(x_input):
    return 1.0 / (1.0 + np.exp(-(np.asarray(x_input, dtype=np.float))))