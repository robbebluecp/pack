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


import numpy as np
from functools import reduce
from collections import Counter

a = ["i have a dream, that's to change the world", "what is the matter guys???", '213456ewyudfhjvc']


def words_mapping(words_list, type=1):
    words_dict = Counter(reduce(lambda x, y: x + y, words_list))
    words_tuple = words_dict.items()
    words_sorted = sorted(words_tuple, key=lambda x: x[1], reverse=True)
    words_sorted_with_index = enumerate(words_sorted)
    char_2_int = {item[1][0]: item[0] for item in words_sorted_with_index}
    int_2_char = {char_2_int[key]: key for key in char_2_int}
    batch_num = len(words_list)
    # one-hot编码
    if type == 1:
        row_num = max(list(map(lambda x: len(x), words_list)))
        col_num = len(words_dict) + 1
        return char_2_int, int_2_char, batch_num, row_num, col_num
    # 常规位置编码
    else:
        col_num = max(list(map(lambda x: len(x), words_list)))
        return char_2_int, int_2_char, batch_num, col_num


def words_encode(words_list, char_2_int=None, int_2_char=None, batch_num=None, col_num=None):
    if not all([char_2_int, int_2_char, batch_num, col_num]):
        char_2_int, int_2_char, batch_num, col_num = words_mapping(words_list, type=2)
    words_encode_list = np.zeros(shape=(batch_num, col_num))

    for batch_index in range(batch_num):
        for col_index in range(len(words_list[batch_index])):
            word = words_list[batch_index][col_index]
            words_encode_list[batch_index][col_index] = char_2_int[word]
    return words_encode_list


def one_hot_encode(words_list, char_2_int=None, int_2_char=None, batch_num=None, row_num=None, col_num=None):
    if not all([char_2_int, int_2_char, batch_num, row_num, col_num]):
        char_2_int, int_2_char, batch_num, row_num, col_num = words_mapping(words_list)
    one_hot_encode_list = np.zeros(shape=(batch_num, row_num, col_num))
    for batch_index in range(batch_num):
        for row_index in range(len(words_list[batch_index])):
            word = words_list[batch_index][row_index]
            one_hot_encode_list[batch_index][row_index][char_2_int[word]] = 1
    return one_hot_encode_list


def words_decode(encode_list, int_2_char):
    decode_list = []
    for batch_index in range(len(encode_list)):
        tmp_str = ''
        for col_index in range(len(encode_list[batch_index])):
            tmp_str += int_2_char[encode_list[batch_index][col_index]]
        decode_list.append(tmp_str)
    return decode_list


def one_hot_decode(one_hot_list, int_2_char):
    one_hot_decode_list = []
    for batch_index in range(len(one_hot_list)):
        tmp_str = ''
        for row_index in range(len(one_hot_list[batch_index])):
            index = np.argmax(one_hot_list[batch_index][row_index])
            tmp_str += int_2_char[index]
        one_hot_decode_list.append(tmp_str)
    return one_hot_decode_list



def softmax(x_input):
    x_input = np.asarray(x_input, dtype=np.float) / max(x_input)
    return np.exp(x_input) / np.sum(np.exp(x_input))


def sigmoid(x_input):
    return 1.0 / (1.0 + np.exp(-(np.asarray(x_input, dtype=np.float))))